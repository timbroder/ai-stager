# Create your views here.
from stager.staging.models import *
from stager.jira.models import *
from stager.jira.forms import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from django.http import HttpResponseRedirect, Http404
from django.views.static import serve
import re
from stager.settings import JIRA_USER, JIRA_PASS, JIRA_WSDL
import SOAPpy, getpass, datetime, array, base64
from SOAPpy import Types
from stager.jira.decorators import *
from django.core.files.uploadedfile import SimpleUploadedFile


@login_required
def list_projects(request, client_path, project_path):
    try:
        client = Client.objects.get(path=client_path)
        project = client.projects.get(path=project_path)

        try:
            jiras = ProjectLink.objects.get(ClientProject=project).JiraProject.exclude(filter_id='')
        except:
            jiras = None
        return render_to_response('jira_list_projects.html', {'project':project, 
                                                                   'client':client,
                                                                   'jiras':jiras, 
                                                                   'user':request.user,
                                                                   'client_path': client_path,
                                                                   'project_path': project_path})
    except Client.DoesNotExist, Project.DoesNotExist:
        raise Http404

    
@login_required
@jira_auth_required
def view_project(request, client_path, project_path, jira_key):
    try:
        client = Client.objects.get(path=client_path)
        project = client.projects.get(path=project_path)

        soap = SOAPpy.WSDL.Proxy(JIRA_WSDL)
        auth = request.session.get('jira_auth')

        jira_project = JiraProject.objects.get(key=jira_key)
        jiras = soap.getIssuesFromFilterWithLimit(auth, "10312", 0, 999)
        
        for jira in jiras:
            test = jira.key.split('-')
            if len(test[1]) == 1:
                pad = "000%s" % test[1]
            elif len(test[1]) == 2:
                pad = "00%s" % test[1]
            elif len(test[1]) == 3:
                pad = "0%s" % test[1]
            else:
                pad = test[1]
                
            jira.key = "%s-%s" % (test[0],pad)
            print jira.key   
            
        
        return render_to_response('jira_project.html', {'project':project, 
                                                                   'client':client,
                                                                   'jiras':jiras, 
                                                                   'jira_project': jira_project,
                                                                   'user':request.user,
                                                                   'client_path': client_path,
                                                                   'project_path': project_path})
    except Client.DoesNotExist, Project.DoesNotExist:
        raise Http404
    
@login_required
@jira_auth_required
def insert_issue(request, client_path, project_path, jira_key):
    try:
        client = Client.objects.get(path=client_path)
        project = client.projects.get(path=project_path)

        soap = SOAPpy.WSDL.Proxy(JIRA_WSDL)
        auth = request.session.get('jira_auth')

        jira_project = JiraProject.objects.get(key=jira_key)

        issue_url = None
        if request.method == 'POST':
            form = JiraTicketForm(request.POST, request.FILES)
            if form.is_valid():
                submitted = True

                newissue = soap.createIssue(auth, {'project': jira_project.key, 
                                                   'type': '1', 
                                                   'description': form.cleaned_data['description'],
                                                   'summary': form.cleaned_data['summary'],
                                                   'customFieldValues': [{'customfieldId': 'customfield_10001',
                                                                          'values': [form.cleaned_data['steps_to_reproduce']]}],
                                                   'assignee': JIRA_USER
                                                   })
                if form.cleaned_data['attachment']:
                    filename="%s" % form.cleaned_data['attachment']
    
                    uploaded = SimpleUploadedFile(filename,
                                             form.cleaned_data['attachment'].read())
    
                    b64t = base64.encodestring(uploaded.read())
                    soap.addBase64EncodedAttachmentsToIssue(auth,
                                               newissue['key'],
                                               [filename],
                                               [b64t])
                issue_url = newissue['key']
        else:
            form = JiraTicketForm()
        
        return render_to_response('jira_create_issue.html', {'project':project, 
                                                                   'client':client,
                                                                   'client_path': client_path,
                                                                   'project_path': project_path,
                                                                   'form': form,
                                                                   'jira_project': jira_project,
                                                                   'user':request.user,
                                                                   'issue_url': issue_url,
                                                                   'jira_key': jira_key})
    except Client.DoesNotExist, Project.DoesNotExist:
        raise Http404