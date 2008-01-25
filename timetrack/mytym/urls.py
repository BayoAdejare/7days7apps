from django.conf.urls.defaults import *

urlpatterns = patterns('mytym.views',
    # Example:
    (r'^$', 'index'),
    (r'^jobs/$', 'handle_jobs'),
    (r'^entries/$', 'handle_entries'),
    (r'^addentry/$', 'detailed_entry'),
    (r'^jobdetails/(?P<id>\d+)/$', 'job_details'),
    (r'^entrydetails/(?P<id>\d+)/$', 'entry_details'),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/djangoprojects/timetrack/mytym/templates/mytym/site_media'}),
    
    )


