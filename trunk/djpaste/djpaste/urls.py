from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djpaste.views',
        (r'^$', 'index'),
        (r'^help/$', direct_to_template, {'template':'djpaste/help.html'}),
        (r'^paste/(?P<id>\d+)/$', 'paste_details'),
        (r'^plain/(?P<id>\d+)/$', 'plain'),
        (r'^html/(?P<id>\d+)/$', 'html'),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/djangoprojects/pastebin/djpaste/templates/djpaste/site_media'}),
    
    )

