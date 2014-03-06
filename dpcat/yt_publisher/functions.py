# encoding: utf-8
import pickle
import base64
import httplib2
from urlparse import urljoin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from oauth2client.client import Storage as BaseStorage, OAuth2WebServerFlow
from oauth2client import xsrfutil
from configuracion import config
import settings

YOUTUBE_SCOPES = [ 'https://www.googleapis.com/auth/youtube.readonly',
                   'https://www.googleapis.com/auth/youtube.upload' ]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class Storage(BaseStorage):

    __STORAGE_OPTION_KEY__ = "YT_PUBLISHER_STORAGE"

    def locked_get(self):
        credential = None

        raw = config.get_option(self.__STORAGE_OPTION_KEY__)
        if raw:
            credential = pickle.loads(base64.b64decode(raw))

        return credential


    def locked_put(self, credentials):
        config.set_option(self.__STORAGE_OPTION_KEY__, base64.b64encode(pickle.dumps(credentials)))

    def locked_delete(self):
        config.del_option(self.__STORAGE_OPTION_KEY__)


def get_flow():
    return OAuth2WebServerFlow(client_id = config.get_option('YT_PUBLISHER_CLIENT_ID'),
                               client_secret = config.get_option('YT_PUBLISHER_CLIENT_SECRET'),
                               scope = YOUTUBE_SCOPES,
                               redirect_uri = urljoin(config.get_option('SITE_URL'), reverse('oauth2callback')))

def get_authenticated_service():
    storage = Storage()
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = get_flow()
        flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, None)
        authorize_url = flow.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http = credentials.authorize(httplib2.Http()))

