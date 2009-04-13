from django.contrib import admin
from stager.staging.models import *
from forms import *
from django.contrib.admin.models import LogEntry

# CLIENT PAGE
class ProjectInline(admin.TabularInline):
    model = Project
    fields = ('name', 'path', 'active')
    template = 'admin/staging/edit_inline/tabular.html'
    modeltype = 'project'


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'path', 'logo', 'active', 'user', 'contact')
    prepopulated_fields = {"path": ("name",)}
    inlines = [ProjectInline,]
    form = ClientLogoSizeAdminForm
    class Media:
        js = ('js/jquery.1.3.1.min.js', 'js/client.js',)


# PROJECT PAGE
class CategoryInline(admin.TabularInline):
    model = Category
    template = 'admin/staging/edit_inline/tabular.html'
    modeltype = 'category'
    
class SectionInline(admin.TabularInline):
    model = Section
    template = 'admin/staging/edit_inline/tabular.html'
    modeltype = 'section'
    fields = ('name', 'category', 'date')
    fk_name = "project"

class ResourcesInline(admin.TabularInline):
    model = Link
    template = 'admin/staging/edit_inline/tabular.html'
    modeltype = 'link'
    verbose_name = "Project Resource"
    verbose_name_plural = "Project Resources"
    fields = ('name', 'remote_link', 'file_link', 'ordering', 'active')   
    form = LinkSizeAdminForm

class ProjectAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('client', 'name', 'path', 'active')
    prepopulated_fields = {"path": ("name",)}
    list_filter = ('client', )
    inlines = [CategoryInline, SectionInline, ResourcesInline]


#SECTION PAGE    
class CompInline(admin.TabularInline):
    model = Comp
    template = 'admin/staging/edit_inline/tabular.html'    
    modeltype = 'comp'
    form = CompSizeAdminForm
    
class SubsectionInline(admin.TabularInline):
    model = Subsection
    template = 'admin/staging/edit_inline/tabular.html'
    modeltype = 'subsection'
    fk_name = "section"

class LinkInline(admin.TabularInline):
    model = Link
    template = 'admin/staging/edit_inline/tabular.html'
    modeltype = 'link'
    fields = ('name', 'remote_link', 'file_link', 'ordering', 'active')
    form = LinkSizeAdminForm

class SectionAdmin(admin.ModelAdmin):
    inlines = [SubsectionInline, CompInline, LinkInline ]


# SUBSECTION PAGE
class SubsectionAdmin(admin.ModelAdmin):
    inlines = [CompInline, LinkInline,]


# COMP PAGE
class SlideInline(admin.TabularInline):
    model = CompSlide
    form = SlideSizeAdminForm

class CompAdmin(admin.ModelAdmin):
    inlines = [SlideInline,]
    form = CompSizeAdminForm


# CONTACT PAGE
class ContactAdmin(admin.ModelAdmin):
    filter_horizontal = ('projects', )

class CompSlideAdmin(admin.ModelAdmin):
    model = CompSlide
    list_display = ('name', 'comp','image')
    form = SlideSizeAdminForm


class LinkAdmin(admin.ModelAdmin):
    form = LinkSizeAdminForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')

class LogEntryAdmin(admin.ModelAdmin):
    model = LogEntry
    list_display = ('object_repr','content_type','user','change_message','action_time')

try:
    admin.site.register(Subsection, SubsectionAdmin)
    admin.site.register(Section, SectionAdmin)
    admin.site.register(Project, ProjectAdmin)
    admin.site.register(Client, ClientAdmin)
    admin.site.register(Contact, ContactAdmin)
    admin.site.register(Category, CategoryAdmin)
    admin.site.register(Link, LinkAdmin)
    admin.site.register(Comp, CompAdmin)
    admin.site.register(CompSlide, CompSlideAdmin)
    admin.site.register(LogEntry, LogEntryAdmin)    
except:
    pass