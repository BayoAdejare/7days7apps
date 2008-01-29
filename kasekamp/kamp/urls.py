from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout, password_change, password_reset

#Account management view
urlpatterns = patterns('',
    url(r'^accounts/login/$',  login, {'template_name': 'registration/login.html'}, 'login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/logout.html'}, 'logout'),                  
    url(r'^accounts/password/reset/$', password_reset, {'template_name': 'registration/password_change.html'}, 'reset'),                  
    url(r'^accounts/password/change/$', password_reset, {'template_name': 'registration/password_change.html'}, 'change'),                  
                )

urlpatterns += patterns('kamp.views',
    # Example:
    (r'^$', 'index'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^(?P<projset>\w+)/$', 'dashboard'),
    (r'^(?P<projset>\w+)/(?P<id>\d+)/$', 'project_summary'),
    (r'^(?P<projset>\w+)/(?P<id>\d+)/milestones/$', 'milestones'),
    (r'^(?P<projset>\w+)/(?P<id>\d+)/todo/$', 'todo'),
    (r'^(?P<projset>\w+)/(?P<id>\d+)/chat/$', 'chat'),
    
    
    (r'^accounts/create/', 'create_user',),
    (r'^foo/$', direct_to_template, {'template':'kamp/base.html'}),
    
) 

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/djangoprojects/kasekamp/kamp/templates/kamp/site_media'}),
    #(r'^admin/', include('django.contrib.admin.urls'),
    )

