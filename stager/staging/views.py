# Create your views here.
from stager.staging.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from django.http import HttpResponseRedirect, Http404
from django.views.static import serve
import re

def check_mobile(request):
    if mobify(request):
		quest = request.get_full_path()
		if quest.find('/why-ai/') == 0:
			pagey = "base_why_ai_mobile.html"
		else:
			pagey = "base_mobile.html"
		return pagey
    else:
	quest = request.get_full_path()
	if quest.find('/why-ai/') == 0:
		pagey = "base_why_ai.html"
	else:
		pagey = 'base.html'
	return pagey

def mobify(request):
	#if request.META.get('HTTP_HOST').find('m.') == 0:
	if request.META.get('QUERY_STRING') == 'mobile':
	#if request.device.get('mobileDevice',None) or request.META.get('HTTP_HOST').find('m.') == 0:
		#return request.device
		return mobify


@login_required
def project(request, client_path, project_path):
    """
    Gets the project view for the specified project.
    """
    try:
        client = Client.objects.get(path=client_path)
        project = client.projects.get(path=project_path)
        return render_to_response('project.html', {'project':project, 'client':client, 'user':request.user, 'check':check_mobile(request),'mobify':mobify(request)})
    except Client.DoesNotExist, Project.DoesNotExist:
        raise Http404

def login(request):
    """
    Basic login.
    """
    error_message = None
    redirect = '/'
    if request.POST:
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                if request.POST.has_key('remember'):
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE) 
                auth.login(request, user)
                return HttpResponseRedirect(request.POST['redirect'])
            else:
                error_message = 'This account has been disabled.'
        else:
            error_message = 'Sorry, that\'s not a valid login.'
        redirect = request.POST['redirect']
    else:
        redirect = request.GET['next']
    
    return render_to_response('login.html', {'message':error_message, 'redirect':redirect})

def logout(request):
    """
    De-authenticates the user.
    """
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login/?next=/')

@login_required
def home(request):
    clients = Client.objects.all().order_by('name')
    try:
        if not request.user.is_staff:
            return client_projects(request, Client.objects.get(user=request.user))
    except:
        pass
        
    return render_to_response('home.html', {'clients': clients, 'user':request.user, 'check':check_mobile(request),'mobify':mobify(request)})

@login_required
def client_projects(request, client_path):
    try:
        client = Client.objects.get(user=request.user)
    except:
        try:
            client = Client.objects.get(path=client_path)
        except Client.DoesNotExist:
            raise Http404
    return render_to_response('client_projects.html', {'client': client, 'user':request.user, 'check':check_mobile(request),'mobify':mobify(request)})

@login_required
def comp_viewer(request, comp_id, idx='0'):
    idx = int(idx)
    comp = Comp.objects.get(id=comp_id)
    if (comp.project.client.user != request.user) and not request.user.is_staff:
        return render_to_response('404.html') 
    if idx == comp.slides.count()-1:
        next = comp.returnlink
    else:
        next = '%s%s/' % (comp.link, idx + 1)

    if idx == 0:
        prev = comp.returnlink
    else:
        prev = '%s%s/' % (comp.link, idx - 1)
        

    try:
        image = comp.slides.all()[idx]
    except:
        image = None

    return render_to_response('compview.html', {'comp':comp, 'slide':image, 'next': next, 
        'prev': prev, 'returnlink': comp.returnlink,'check':check_mobile(request),'mobify':mobify(request)})
    
def error(request):
    return render_to_response('404.html') 

@login_required
def servefile(request, filename):
        if re.search("/" + settings.MEDIA_PREFIX + "/" + settings.FILE_UPLOAD + "/", request.path):
            if (Client.objects.filter(path=request.path.split("/")[3]).get().user != request.user) and not request.user.is_staff:
                return render_to_response('404.html') 
        return serve(request, filename, document_root=settings.MEDIA_ROOT+"/"+settings.FILE_UPLOAD)