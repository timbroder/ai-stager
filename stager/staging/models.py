from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import os
from stager.widgets import ColorPickerWidget

class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super(ColorField, self).formfield(**kwargs)

def get_comp_path(instance, filename):
    return settings.FILE_UPLOAD + "/" + \
        instance.project.client.path + "/" + \
        instance.project.path + "/comps/" + filename

def get_slide_path(instance, filename):
    return settings.FILE_UPLOAD + "/" + \
        instance.comp.project.client.path + "/" + \
        instance.comp.project.path + "/comps/" + filename

def get_logo_path(instance, filename):
    return settings.FILE_UPLOAD + "/" + instance.path + "/" + filename

def get_link_path(instance, filename):
    return settings.FILE_UPLOAD + "/" + \
        instance.project.project.client.path + "/" + \
        instance.project.project.path + filename

class Client(models.Model):
    """
    A client.
    """
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    path = models.CharField('URL fragment', 
        help_text='<a href="' + settings.BASE_URL + 'url_fragment/" \
                   target="_new" id="url_fragment">' + settings.BASE_URL + 'url_fragment/</a>', max_length=100, unique=True)
    logo = models.ImageField(upload_to=get_logo_path, help_text="( Width = 200, Height = 55 )", blank=True, null=True)
    user = models.ForeignKey(User,related_name='users')
    contact = models.ForeignKey('Contact', related_name='clients',  blank=True, null=True, 
        help_text='The PM. (shows up on the internal homepage)')

    def __unicode__(self):
        return self.name
    
    @property
    def has_multiple_projects(self):
        """
        Returns true if there is more than one active project associated with this client.
        """
        return self.projects.filter(active=True).count() > 1
    
    @property
    def active_projects(self):
        """
        Returns the active projects for the client.
        """
        return self.projects.filter(active=True)
        
    def link(self):
        return "/" + self.path + "/"

class Container(models.Model):
    name = models.CharField(blank=False, max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
class Project(Container):
    """
    A project.
    """
    client = models.ForeignKey(Client, related_name='projects')
    path = models.CharField('URL fragment',
        help_text=settings.BASE_URL + 'client/url_fragment/', max_length=100)
    
    def __unicode__(self):
        return '%s - %s' % (self.client.name,self.name)
    
    @property
    def ai_contacts(self):
        return self.contacts.filter(ai_staff=True).filter(active=True)
    
    @property
    def client_contacts(self):
        return self.contacts.filter(ai_staff=False).filter(active=True)
    
    @property
    def active_sections(self):
        return self.sections.filter(active=True).order_by('-date')
    
    @property
    def category_rollups(self):
        return [CategoryRollup(category,self.active_sections.filter(category=category)) for category in self.categories.all()]

    @property
    def link(self):
        return "/clients/" # + self.client.path + "/" + self.path + "/"

    @property
    def default_category(self):
        try: 
            return slugify(self.categories.filter(project=self).filter(default=True)[:1][0].name)
        except:
            try:
                return  slugify(self.categories.filter(project=self)[:1][0].name)
            except:
                return 0

class Contact(models.Model):
    """
    A contact on the project.
    """
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    telephone = models.CharField(blank=True, max_length=100)
    title = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    projects = models.ManyToManyField(Project,related_name='contacts')
    active = models.BooleanField(default=True)
    ai_staff = models.BooleanField()
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s %s' % (self.first_name,self.last_name)

    class Meta:
        ordering = ['ordering']

class Category(models.Model):
    """
    A category of info for a project.
    """
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project,related_name='categories')
    ordering = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    default = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s : %s' % (self.project.id, self.name, )

    def save(self, force_insert=False, force_update=False):
        if self.default:
          Category.objects.filter(project=self.project).update(default=None)
        super(Category, self).save(force_insert, force_update)

    class Meta:
        ordering = ['ordering']
        verbose_name_plural = 'categories'


class Section(Container):
    """
    A section of a project.
    """
    project = models.ForeignKey(Project,related_name='sections')
    date = models.DateField(auto_now_add=False)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name
    
    @property
    def active_links(self):
        return self.links.filter(active=True)
    
    @property
    def active_subsections(self):
        return self.subsections.filter(active=True)

    class Meta:
        ordering = ['date']

class Subsection(Container):
    """
    A subsection of a section.
    """
    section = models.ForeignKey(Container,related_name='subsections')
    
    def __unicode__(self):
        return self.name
    
    @property
    def active_links(self):
        return  self.links.filter(active=True)
    

class Link(models.Model):
    """
    A link to a file.
    """
    remote_link = models.URLField(blank=True, null=True, verify_exists=False)
    file_link = models.FileField(upload_to=get_link_path,blank=True,null=True)
    linked = models.ForeignKey(Container, related_name="links", blank=False, null=False)
    name = models.CharField(blank=True, max_length=100)
    active = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
    @property
    def link(self):
        if self.file_link:
            return '%s%s' % (settings.MEDIA_URL, self.file_link)
        else:
            return self.remote_link

    @property
    def project(self):
        try:
            return self.linked.section.section.project
        except:
            try:
                return self.linked.subsection.section.section.project
            except:
                return self.linked.project

    class Meta:
        ordering = ['ordering', ]

        
        
class Comp(models.Model):
    """
    A Link to a comp
    """
    name = models.CharField(max_length=128)
    background = models.ImageField(upload_to=get_comp_path, blank=True, null=True)
    remove_background = models.BooleanField('Remove Background')
    background_colorfield = ColorField(blank=True) 
    ordering = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    linked = models.ForeignKey(Container, related_name="comps", blank=False, null=False)
    
    @property
    def link(self):
        project = self.project
        return '/client/%s/%s/comps/%s/' % (project.client.path, project.path, self.id )

    @property
    def project(self):
        try:
            return self.linked.section.section.project
        except:
            try:
                return self.linked.subsection.section.section.project
            except:
                return self.linked.project
    
    @property
    def category(self):
        try:
            return self.linked.section.category.name
        except:
            return self.linked.subsection.section.section.category.name
    
    @property
    def returnlink(self):
        project = self.project
        return '/client/%s/%s/#%s_category' % (project.client.path, 
                                               project.path, 
                                               slugify(self.category))
    def __unicode__(self):
        return self.name
        
    def save(self):
        if self.remove_background and self.background != "" and self.background:
            if os.path.exists(self.background.path):
                os.remove(self.background.path)
            self.background = ""
        self.remove_background = False
                
        super(Comp, self).save()

    class Meta:
        ordering = ['ordering', ]

    
class CompSlide(models.Model):
    ALIGNMENT_CHOICES = (
        ('left','left'),
        ('right','right'),
    )
    name = models.CharField(max_length=128)
    comp = models.ForeignKey(Comp, related_name="slides")
    image = models.ImageField(upload_to=get_slide_path, blank=True, null=True)
    alignment = models.CharField(max_length=128, choices=ALIGNMENT_CHOICES, blank=True, null=True)
    backgroundfield = models.ImageField(upload_to=get_slide_path, blank=True, null=True)
    remove_background = models.BooleanField('Remove Background')
    background_colorfield = ColorField(blank=True) 
    active = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0)
    
    @property
    def background(self):
        return self.backgroundfield or self.comp.background or None

    @property
    def background_color(self):
        return self.background_colorfield or self.comp.background_colorfield or "#FFFFFF"

    def __unicode__(self):
        return self.comp.name 

    def save(self):
        if self.remove_background and self.backgroundfield != "" and self.backgroundfield:
            if os.path.exists(self.backgroundfield.path):
                os.remove(self.backgroundfield.path)
            self.backgroundfield = ""
        self.remove_background = False
                
        super(CompSlide, self).save()


        
    class Meta:
        ordering = ['ordering', ]

class CategoryRollup(object):
    """
    Convenience object to roll up categories.
    """
    def __init__(self,category,sections):
        self.category = category
        self.sections = sections

class ViewChoice(models.Model):
    default_d = models.TextField(choices = (('grid', 'grid'), ('list','list'))) 
     
    def __unicode__(self):
        return self.default_d

class UserPreference(models.Model):
    """This class will add features to Django's User class using a connecting one-to-one field on the User Model"""
    default_display = models.ForeignKey(ViewChoice, default = ViewChoice.objects.get(id=1).id)
    user = models.OneToOneField(User, unique=True, related_name='userschoices')

    def __unicode__(self):
	return self.user.username + "'s viewing choice"

