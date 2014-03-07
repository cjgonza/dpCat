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


def get_flow():
    return OAuth2WebServerFlow(client_id = config.get_option('YT_PUBLISHER_CLIENT_ID'),
                               client_secret = config.get_option('YT_PUBLISHER_CLIENT_SECRET'),
                               scope = YOUTUBE_SCOPES,
                               redirect_uri = urljoin(config.get_option('SITE_URL'), reverse('oauth2callback')))
