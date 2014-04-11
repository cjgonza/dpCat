# encoding: utf-8

import httplib
import httplib2
import random
import time
import json
import tempfile
import os
from cgi import escape

from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload

from settings import MEDIA_ROOT
from postproduccion.models import RegistroPublicacion
from yt_publisher.functions import get_authenticated_service, create_playlist, insert_video_in_playlist

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# Categoría de publicación en YouTube (Formación).
PUBLICATION_CATEGORY = 27

# Estado de privacidad de la publicación
#PRIVACY_STATUS = 'public'
PRIVACY_STATUS = 'unlisted'

# Patrón de la URL de los vídeos publicados
PUBLISHED_PATTERN_URL = 'http://www.youtube.com/watch?v=%s'

def publish(task):
    task.set_status('EXE') # esto se debería hacer desde fuera en caso de multithread.
    v = task.video
    d = json.loads(task.data)

    body = dict(
        snippet = dict(
            title = escape(d['title']),
            description = escape(d['description']),
            tags = escape(d['tags']).split(','),
            categoryId = PUBLICATION_CATEGORY
        ),
        status = dict(
            privacyStatus = PRIVACY_STATUS
        )
    )

    insert_request = get_authenticated_service().videos().insert(
        part = ",".join(body.keys()),
        body = body,
        fields = "id",
        media_body = MediaFileUpload(task.video.fichero, chunksize = -1, resumable = True)
    )

    messages = str()
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            status, response = insert_request.next_chunk()
            if 'id' in response:
                # Vídeo subido correctamente
                videoid = response['id']
                messages += "Video id '%s' was successfully uploaded.\n" % videoid
                RegistroPublicacion(video = v, enlace = PUBLISHED_PATTERN_URL % videoid).save()
                task.delete()

                # Se crea o inserta una lista de reproducción si es necesario.
                if d['playlist']:
                    if d['playlist'] == 1:
                        playlistid = d['add_to_playlist']
                    else:
                        playlistid = create_playlist(escape(d['new_playlist_name']), escape(d['new_playlist_description']), PRIVACY_STATUS)
                    insert_video_in_playlist(videoid, playlistid)
                return
            else:
                messages += "The upload failed with an unexpected response: %s\n" % response
                create_error_logfile(task, messages)
                task.set_status('ERR')
                return
        except HttpError, e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s\n" % (e.resp.status, e.content)
            else:
                messages += "A HTTP error %d occurred:\n%s\n" % (e.resp.status, e.content)
                create_error_logfile(task, messages)
                task.set_status('ERR')
                return
        except RETRIABLE_EXCEPTIONS, e:
            error = "A retriable error occurred: %s\n" % e
        except Exception, e:
            error = "Unexpected Error:\n  %s: %s\n" % (type(e).__name__, e)
            create_error_logfile(task, messages)
            task.set_status('ERR')
            return

        if error is not None:
            messages += error
            retry += 1
            if retry > MAX_RETRIES:
                messages += "No longer attempting to retry.\n"
                create_error_logfile(task, messages)
                task.set_status('ERR')
                return

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            messages += "Sleeping %f seconds and then retrying...\n" % sleep_seconds
            time.sleep(sleep_seconds)

def create_error_logfile(task, error_text):
    (handle, path) = tempfile.mkstemp(suffix = '.yt-pub.log', dir = MEDIA_ROOT + '/' + task.logfile.field.get_directory_name())
    task.logfile = task.logfile.field.get_directory_name() + '/' + os.path.basename(path)
    os.write(handle, error_text.encode('utf-8'))
    os.close(handle)
