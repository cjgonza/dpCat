from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^postproduccion/', include('postproduccion.urls')),
    (r'^admin/', include(admin.site.urls)),
)
