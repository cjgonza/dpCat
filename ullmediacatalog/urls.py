from django.conf.urls.defaults import *
from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'postproduccion.views.index'),
    (r'^postproduccion/', include('postproduccion.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    #(r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,'show_indexes':True}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name' : 'postproduccion/login.html'}),
)
