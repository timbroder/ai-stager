from django.db import models
from stager.staging.models import *

class JiraProject(models.Model):
    key = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    filter_id = models.CharField(max_length=255)
    updated = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
class JiraStatus(models.Model):
    key = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    updated = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
class JiraType(models.Model):
    key = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    updated = models.IntegerField(default=0)
    allowed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class ProjectLink(models.Model):
    ClientProject = models.ForeignKey(Project, unique=True)
    JiraProject = models.ManyToManyField(JiraProject)
   
    def __unicode__(self):
        return self.ClientProject.name