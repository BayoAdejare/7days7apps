from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout

#Account management view
urlpatterns = patterns('',
    url(r'^accounts/login/$',  login, {'template_name': 'registration/login.html'}, 'login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/logout.html'}, 'logout')                                   
                )

urlpatterns += patterns('answrs.views',
    # Example:
    # (r'^answers/', include('answers.foo.urls')),
    (r'^$', 'index'),
    (r'^random/$', 'randompage'),
    (r'^about/$', direct_to_template, {'template':'answrs/about.html'}),
    (r'^ask/$', 'ask'),
    (r'^ask/(?P<category_slug>[^\.^/]+)/$', 'ask'),
    (r'answer/(?P<id>\d+)/', 'answer'),
    (r'close/(?P<id>\d+)/', 'close'),
    (r'bestify/(?P<id>\d+)/', 'bestify'),
    (r'^addcat/$', 'add_cat'),
    (r'^cat/(?P<slug>[^\.^/]+)/$', 'view_cat'),
    (r'^profile/(?P<username>\w+)/', 'profile'),
    (r'^accounts/profile/', 'profile'),
    (r'^accounts/create/', 'create_user'),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/djangoprojects/answers/answrs/site_media'}),
    )

