from django.conf.urls.defaults import *


urlpatterns = patterns('postproduccion.views',
    (r'^$', 'index'),
    (r'^crear/$', 'crear'),
    (r'^(?P<video_id>\d+)/fichero_entrada/$', 'fichero_entrada'),
    (r'^dirlist/$', 'dirlist'),
    (r'^cola/$', 'cola_base'),
    (r'^cola_listado/$', 'cola_listado'),
    (r'^(?P<task_id>\d+)/mostrar_log/$', 'mostrar_log'),
    (r'^(?P<tk_str>\w{25})/definir_metadatos/$', 'definir_metadatos_user'),
    (r'^(?P<video_id>\d+)/definir_metadatos/$', 'definir_metadatos_oper'),
    (r'^(?P<tk_str>\w{25})/aprobacion_video/$', 'aprobacion_video'),
    (r'^(?P<tk_str>\w{25})/rechazar_video/$', 'rechazar_video'),
    (r'^(?P<video_id>\d+)/stream.mp4$', 'stream_video'),
    (r'^(?P<tk_str>\w{25})/stream.flv$', 'stream_preview'),
)
