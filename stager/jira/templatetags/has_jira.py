from django import template
from stager.jira.models import JiraProject, ProjectLink
from stager.staging.models import *

register = template.Library()

def has_jira(value, arg):
    "Removes all values of arg from the given string"
    #project = Project.objects.get(name=value)
    print value
    client = Client.objects.get(path=value)
    project = client.projects.get(path=arg)
    try:
        jiras = ProjectLink.objects.get(ClientProject=project).JiraProject.exclude(filter_id='')
        return True
    except:
        return False

register.filter('has_jira', has_jira)
