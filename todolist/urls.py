from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_change, password_reset

#Account management view
urlpatterns = patterns('',
    url(r'^accounts/login/$',  login, {'template_name': 'registration/login.html'}, 'login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/logout.html'}, 'logout'),                  
    url(r'^accounts/password/reset/$', password_reset, {'template_name': 'registration/password_change.html'}, 'reset'),                  
    url(r'^accounts/password/change/$', password_reset, {'template_name': 'registration/password_change.html'}, 'change'),                  
                )

urlpatterns += patterns('',
    (r'^', include('todolist.todidlist.urls')),
)



