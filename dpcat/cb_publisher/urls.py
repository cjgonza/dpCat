from django.conf.urls.defaults import *


urlpatterns = patterns('cb_publisher.views',
    url(r'^config_plugin/$', 'config_plugin', name = "config_plugin"),
    url(r'^publicar/(?P<video_id>\d+)/$', 'publicar', name = "publicar"),
)
