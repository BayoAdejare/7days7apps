from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('jobs.views',
    # Example:
    (r'^$', 'index'),
    (r'^adddev/$', 'add_developer'),
    (r'^addjob/$', 'add_job'),
    (r'^developers/$', 'developers'),
    (r'^jobs/$', 'jobs'),
    (r'^job/(?P<id>\d+)/$', 'job'),
    (r'^editjob/(?P<id>\d+)/$', 'edit_job'),
    (r'^editjob/(?P<id>\d+)/done/$', 'edit_job_done'),
    (r'^developer/(?P<id>\d+)/$', 'developer'),
    (r'^editdev/(?P<id>\d+)/$', 'edit_developer'),
    (r'^editdev/(?P<id>\d+)/done/$', 'edit_developer_done'),
    (r'^about/$', direct_to_template, {'template':'jobs/about.html'}),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/djangoprojects/djobboard/jobs/templates/jobs'}), 
    )


