from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^', include('pastebin.djpaste.urls'))
    # (r'^pastebin/', include('pastebin.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
