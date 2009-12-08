from django import forms
from stager.jira.models import *
from django.utils.functional import lazy


def type_choices():
    return [(type.key, type.name) for type in JiraType.objects.filter(allowed=True)]

class JiraTicketForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(JiraTicketForm, self).__init__(*args, **kwargs)
        self.fields['issue_type'] = forms.ChoiceField(choices=type_choices())
        self.fields['description'] = forms.CharField(widget=forms.Textarea)
        self.fields['steps_to_reproduce'] = forms.CharField(widget=forms.Textarea)
        self.fields['attachment'] = forms.FileField(required=False)
    summary = forms.CharField(widget=forms.Textarea)

#choices=[('bug', 'Bug'),
#          ('feature', 'New Feature')])


