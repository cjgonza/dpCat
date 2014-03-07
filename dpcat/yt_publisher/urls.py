from django.conf.urls.defaults import *


urlpatterns = patterns('yt_publisher.views',
    url(r'^config_plugin/$', 'config_plugin', name = "config_plugin"),
    url(r'^authorize/$', 'auth_manage', name = "authorize"),
    url(r'^revoke/$', 'auth_manage', { 'revoke' : True }, name = "revoke"),
    #url(r'^publicar/(?P<video_id>\d+)/$', 'publicar', name = "publicar"),
    #url(r'^cola/$', 'cola_publicacion', name = "cola_publicacion"),
    #url(r'^contenido_cola/$', 'contenido_cola_publicacion', name = "contenido_cola_publicacion"),
    #url(r'^purgar_publicaciones/$', 'purgar_publicaciones', name = "purgar_publicaciones"),
    url(r'^oauth2callback', 'auth_return', name = "oauth2callback"),
)
