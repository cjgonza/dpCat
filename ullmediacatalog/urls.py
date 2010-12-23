from django.conf.urls.defaults import *
from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^postproduccion/', include('postproduccion.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JQUERY_ROOT}),
)
