from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^answers/', include('answers.foo.urls')),
    (r'', include('answers.answrs.urls')),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
