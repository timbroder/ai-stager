from django.contrib import admin
from django.contrib.admin.models import LogEntry
from stager.jira.models import *

class JiraProjectAdmin(admin.ModelAdmin):
    ordering = ['name']
    fields = ('key', 'name', 'filter_id')
    
class JiraTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'allowed',)
    
admin.site.register(JiraProject, JiraProjectAdmin)
admin.site.register(ProjectLink)
admin.site.register(JiraType,JiraTypeAdmin)