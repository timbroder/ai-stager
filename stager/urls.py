""" urls.py """
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

handler404 = 'stager.staging.views.error'
handler500 = 'stager.staging.views.error'

urlpatterns = patterns('',
    url(r'^admin/export/', include('stager.export.urls')),
)

urlpatterns += patterns('stager.staging.views',
    (r'^home/$','home'),

    (r'^accounts/login/$','login'),
    (r'^login/$','login'),
    (r'^logout/$','logout'),
    
    (r'^admin/(.*)', admin.site.root),

    # Protect assets (make sure apache does not serve this directory)
    (r'^static/'+settings.FILE_UPLOAD+'(?P<filename>.*)$', 'servefile'),

    (r'^$', 'home'),

    (r'^client/(.*)/(.*)/comps/(?P<comp_id>\w+)/$', 'comp_viewer'),
    (r'^client/(.*)/(.*)/comps/(?P<comp_id>\w+)/(?P<idx>\d+)/$', 'comp_viewer'),
    (r'^client/(?P<client_path>.*)/(?P<project_path>.*)/$', 'project'),
    (r'^client/(?P<client_path>\w+)/$', 'client_projects'),
    (r'(?P<client_path>\w+)/$',  'client_projects'),
)



if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^static/(.*)$','serve',{'document_root':settings.MEDIA_ROOT}),
    )