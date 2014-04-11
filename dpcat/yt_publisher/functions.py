# encoding: utf-8
import pickle
import base64
import httplib2
from urlparse import urljoin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from oauth2client.client import Storage as BaseStorage, OAuth2WebServerFlow, Error
from oauth2client import xsrfutil
from apiclient.discovery import build
from yt_publisher.models import Publicacion
from configuracion import config
import settings

YOUTUBE_SCOPES = [ 'https://www.googleapis.com/auth/youtubepartner',
                   'https://www.googleapis.com/auth/youtube.upload' ]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

LICENSE_TEXTS = {
    'CR' : 'Todos los derechos reservados.',
    'MD' : 'Creative Commons: Reconocimiento - No Comercial (CC BY NC).\nhttp://creativecommons.org/licenses/by-nc/4.0/deed.es_ES',
    'SA' : 'Creative Commons: Reconocimiento - No Comercial - Compartir Igual (CC BY NC SA).\nhttp://creativecommons.org/licenses/by-nc-sa/4.0/deed.es_ES',
    'ND' : 'Creative Commons: Reconocimiento - No Comercial - Sin Obra Derivada (CC BY NC ND).\nhttp://creativecommons.org/licenses/by-nc-nd/4.0/deed.es_ES'
}

class Storage(BaseStorage):

    __STORAGE_OPTION_KEY__ = "YT_PUBLISHER_STORAGE"

    def locked_get(self):
        credentials = None

        raw = config.get_option(self.__STORAGE_OPTION_KEY__)
        if raw:
            credentials = pickle.loads(base64.b64decode(raw))
            credentials.set_store(self)

        return credentials


    def locked_put(self, credentials):
        config.set_option(self.__STORAGE_OPTION_KEY__, base64.b64encode(pickle.dumps(credentials)))

    def locked_delete(self):
        config.del_option(self.__STORAGE_OPTION_KEY__)

class UnauthorizedError(Error):
    pass

def get_flow():
    return OAuth2WebServerFlow(client_id = config.get_option('YT_PUBLISHER_CLIENT_ID'),
                               client_secret = config.get_option('YT_PUBLISHER_CLIENT_SECRET'),
                               scope = YOUTUBE_SCOPES,
                               redirect_uri = urljoin(config.get_option('SITE_URL'), reverse('oauth2callback')),
                               access_type = 'offline')


def get_authenticated_service():
    credential = Storage().get()
    if credential is None or credential.invalid == True:
        raise UnauthorizedError
    http = httplib2.Http()
    http = credential.authorize(http)
    return build("youtube", "v3", http=http)

def get_playlists():
    youtube = get_authenticated_service()

    data = list()

    next_page_token = ""
    while next_page_token is not None:
        playlists_response = youtube.playlists().list(
          mine=True,
          part="snippet",
          maxResults=50,
          fields="items(id,snippet(title)),nextPageToken",
          pageToken=next_page_token
        ).execute()

        for playlist in playlists_response["items"]:
            data.append((playlist['id'], playlist['snippet']['title']))

        next_page_token = playlists_response.get("nextPageToken")

    return data

def create_playlist(title, description, privacy_status):
    youtube = get_authenticated_service()

    playlists_insert_response = youtube.playlists().insert(
        part = "snippet,status",
        body = dict(
            snippet = dict(
                title = title,
                description = description
            ),
            status = dict(
                privacyStatus = privacy_status
            )
        ),
        fields = "id"
    ).execute()

    return playlists_insert_response["id"]

def insert_video_in_playlist(videoid, playlistid):
    youtube = get_authenticated_service()

    youtube.playlistItems().insert(
        part = "snippet",
        body = dict(
            snippet = dict(
                playlistId = playlistid,
                resourceId = dict(
                    kind = 'youtube#video',
                    videoId = videoid
                )
            )
        ),
        fields = ""
    ).execute()

def error_handler(e, request):
    try:
        raise e
    except UnauthorizedError:
        messages.error(request, u'No existe una cuenta asociada para la publicación, debe configurar una para poder publicar')
        return HttpResponseRedirect(reverse("config_plugin"))
    except Error:
        credentials = Storage().get()
        credentials.revoke(httplib2.Http())
        messages.error(request, u'Ha habido un error con cuenta de publicación, se debe volver a realizar la asociación')
        return HttpResponseRedirect(reverse("config_plugin"))

"""
Devuelve el número de puestos libres para iniciar el proceso de publicación.
"""
def available_slots():
    return int(config.get_option('YT_PUBLISHER_MAX_TASKS')) - Publicacion.objects.count_actives()
