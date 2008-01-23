from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('todidlist.views',
    url(r'^$', 'index', name = 'index'),
    url(r'^create/$', 'create', name='create'),
    url(r'^list/(?P<list_id>\d+)/$', 'list_detail', name='list_detail'),
    url(r'^edit/(?P<list_id>\d+)/$', 'edit_detail', name='edit_detail'),
    url(r'^edititem/(?P<item_id>\d+)/$', 'edit_item', name='edit_item'),
    url(r'^viewitem/(?P<item_id>\d+)/$', 'view_item', name='view_item'),    
    url(r'^admin/', include('django.contrib.admin.urls')),
    url(r'^accounts/profile/$', 'manage', name="profile"),
    url(r'^accounts/create/$', 'create_user', name="create_user"),
    url(r'^not/$', direct_to_template, {'template':'todidlist/not.html'}, name='not'),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/djangoprojects/todolist/todidlist/templates/todidlist/site_media'}),
    
    )
