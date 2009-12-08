from django import template
from stager.jira.models import JiraStatus

register = template.Library()

def status_string(value):
    "Removes all values of arg from the given string"
    return JiraStatus.objects.get(key=value)

register.filter('status_string', status_string)
