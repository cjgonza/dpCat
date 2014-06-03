from django.conf.urls import patterns, include, url


urlpatterns = patterns('cb_publisher.views',
    url(r'^config_plugin/$', 'config_plugin', name = "config_plugin"),
    url(r'^publicar/(?P<video_id>\d+)/$', 'publicar', name = "publicar"),
    url(r'^cola/$', 'cola_publicacion', name = "cola_publicacion"),
    url(r'^contenido_cola/$', 'contenido_cola_publicacion', name = "contenido_cola_publicacion"),
    url(r'^purgar_publicaciones/$', 'purgar_publicaciones', name = "purgar_publicaciones"),
)
