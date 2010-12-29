from django.conf.urls.defaults import *


urlpatterns = patterns('postproduccion.views',
    (r'^crear/$', 'crear'),
    (r'^(?P<video_id>\d+)/fichero_entrada/$', 'fichero_entrada'),
    (r'^dirlist/$', 'dirlist'),
    (r'^cola/$', 'cola_base'),
    (r'^cola_listado/$', 'cola_listado'),
)
