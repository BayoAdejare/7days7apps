from django.conf.urls.defaults import *

urlpatterns = patterns('pollngo.views',
    (r'^$', 'index'),
    (r'^poll/(?P<slug>[^\.^/]+)/$', 'question'),
    (r'^create/$', 'create'),
    (r'^results/(?P<slug>[^\.^/]+)/$', 'results'),
    )

urlpatterns += patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    )

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/djangoprojects/polls/templates/site_media'}),
    
    )