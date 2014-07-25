from django.conf.urls import patterns, include, url
from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'postproduccion.views.index'),
    (r'^postproduccion/', include('postproduccion.urls')),
    #(r'^cb_publisher/', include('cb_publisher.urls')),
    (r'^yt_publisher/', include('yt_publisher.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', { 'next_page' : '/'}),
)
