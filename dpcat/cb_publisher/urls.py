from django.conf.urls.defaults import *


urlpatterns = patterns('cb_publisher.views',
    url(r'^config_plugin/$', 'config_plugin', name = "config_plugin"),
    url(r'^publicar/(?P<video_id>\d+)/$', 'publicar', name = "publicar"),
    url(r'^cola/$', 'cola_publicacion', name = "cola_publicacion"),
    url(r'^contenido_cola/$', 'contenido_cola_publicacion', name = "contenido_cola_publicacion"),
    url(r'^purgar_publicaciones/$', 'purgar_publicaciones', name = "purgar_publicaciones"),
    url(r'^borrar_registro/(?P<record_id>\d+)/$', 'borrar_registro', name = "borrar_registro"),
    url(r'^notificar/(?P<record_id>\d+)/$', 'notificar_publicacion', name = "notificar_publicacion"),
)
