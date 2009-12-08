from django.core.management.base import NoArgsCommand
from django.conf import settings
import SOAPpy, getpass, datetime
from settings import JIRA_USER, JIRA_PASS, JIRA_WSDL
from jira.models import *

class Command(NoArgsCommand):
    help = "Removes CompSlides from the database that do not have matching files on the drive."

    def listSOAPmethods(self,soap):
        for key in soap.methods.keys():
            print key, ': '
            for param in soap.methods[key].inparams:
                print '\t', param.name.ljust(10), param.type
            for param in soap.methods[key].outparams:
                print '\tOut: ', param.name.ljust(10), param.type

    def handle_noargs(self, **options):
        soap = SOAPpy.WSDL.Proxy(JIRA_WSDL)
        #self.listSOAPmethods(soap)
        auth = soap.login(JIRA_USER, JIRA_PASS)
        try:
            updated = JiraProject.objects.all()[0].updated + 1
        except IndexError:
            updated = 1

        
        projects = soap.getProjectsNoSchemes(auth)
        print len(projects)
        for project in projects:
            print "%s - %s" % (project['key'], project['name'])
            
            try:
                jira = JiraProject.objects.get(key=project['key'])
                jira.name = project['name']
                jira.updated = updated
            except:
                jira = JiraProject(key=project['key'], name=project['name'], updated=updated)
            jira.save()
       
        
        try:
            updated = JiraType.objects.all()[0].updated + 1
        except IndexError:
            updated = 1
        statuses = soap.getIssueTypes(auth)
        for status in statuses:
            print "%s - %s" % (status['id'], status['name'])
            
            try:
                s = JiraType.objects.get(key=status['id'])
                s.name = status['name']
                s.updated = updated
            except:
                s = JiraType(key=status['id'], name=status['name'], updated=updated)
            s.save()
        
        #removed closed projects
        JiraType.objects.exclude(updated=updated).delete()

        try:
            updated = JiraStatus.objects.all()[0].updated + 1
        except IndexError:
            updated = 1
        statuses = soap.getStatuses(auth)
        for status in statuses:
            print "%s - %s" % (status['id'], status['name'])
            
            try:
                s = JiraStatus.objects.get(key=status['id'])
                s.name = status['name']
                s.updated = updated
            except:
                s = JiraStatus(key=status['id'], name=status['name'], updated=updated)
            s.save()
        
        #removed closed projects
        JiraStatus.objects.exclude(updated=updated).delete()