from django.conf.urls.defaults import *


urlpatterns = patterns('postproduccion.views',
    (r'^$', 'index'),
    (r'^crear/$', 'crear'),
    (r'^fichero_entrada/(?P<video_id>\d+)/$', 'fichero_entrada'),
    (r'^dirlist/$', 'dirlist'),
    (r'^cola/$', 'cola_base'),
    (r'^cola_listado/$', 'cola_listado'),
    (r'^mostrar_log/(?P<task_id>\d+)/$', 'mostrar_log'),
    (r'^definir_metadatos/(?P<tk_str>\w{25})/$', 'definir_metadatos_user'),
    (r'^definir_metadatos/(?P<video_id>\d+)/$', 'definir_metadatos_oper'),
    (r'^aprobacion_video/(?P<tk_str>\w{25})/$', 'aprobacion_video'),
    (r'^rechazar_video/(?P<tk_str>\w{25})/$', 'rechazar_video'),
    (r'^stream/(?P<video_id>\d+).mp4$', 'stream_video'),
    (r'^stream/(?P<tk_str>\w{25}).flv$', 'stream_preview'),
    (r'^enproceso/$', 'listar_en_proceso'),
    (r'^pendientes/$', 'listar_pendientes'),
    (r'^log/$', 'showlog'),
    (r'^log/old/$', 'showlog', { 'old' : True }),
)
