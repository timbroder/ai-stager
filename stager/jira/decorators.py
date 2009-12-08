from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from settings import JIRA_USER, JIRA_PASS, JIRA_WSDL
import SOAPpy

def jira_auth_required(function=None):
    def wrap(request, *args, **kwargs):
        soap = SOAPpy.WSDL.Proxy(JIRA_WSDL)
        auth = soap.login(JIRA_USER, JIRA_PASS)
        request.session['jira_auth'] = auth
        return function(request, *args, **kwargs)

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap
