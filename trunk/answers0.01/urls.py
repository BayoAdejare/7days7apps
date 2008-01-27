from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^answers/', include('answers.foo.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'', include('answers.answrs.urls')),

    # Uncomment this for admin:
)
