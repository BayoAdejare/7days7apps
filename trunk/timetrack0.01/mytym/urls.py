from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template

urlpatterns = patterns('mytym.views',
    # Example:
    (r'^$', 'index'),
    (r'^help/$', direct_to_template, {'template':'mytym/about.html'}),
    (r'^jobs/$', 'handle_jobs'),
    (r'^entries/$', 'handle_entries'),
    (r'^addentry/$', 'detailed_entry'),
    (r'^jobdetails/(?P<id>\d+)/$', 'job_details'),
    (r'^entrydetails/(?P<id>\d+)/$', 'entry_details'),
    (r'^category/(?P<id>\d+)/$', 'category'),
    (r'^stats/$', 'stats'),
    (r'^accounts/profile/$', redirect_to, {'url':'/'}),
    (r'^accounts/register/$', 'create_user',),
    

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/djangoprojects/timetrack/mytym/templates/mytym/site_media'}),
    
    )


