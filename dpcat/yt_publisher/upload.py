# encoding: utf-8

import httplib
import httplib2
import random
import time
import json

from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload

from postproduccion.models import RegistroPublicacion
from yt_publisher.functions import get_authenticated_service

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

def publish(task):
    task.status = 'EXE' # esto se debería hacer desde fuera en caso de multithread.
    task.save()
    v = task.video
    d = json.loads(task.data)

    body = dict(
        snippet = dict(
            title = d['title'],
            description = d['description'],
            tags = d['tags'].split(','),
            categoryId = PUBLICATION_CATEGORY
        ),
        status = dict(
            privacyStatus = PRIVACY_STATUS
        )
    )

    insert_request = get_authenticated_service().videos().insert(
        part = ",".join(body.keys()),
        body = body,
        media_body = MediaFileUpload(task.video.fichero, chunksize = -1, resumable = True)
    )

    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print "Uploading file..."
            status, response = insert_request.next_chunk()
            if 'id' in response:
                print "Video id '%s' was successfully uploaded." % response['id']
            else:
                exit("The upload failed with an unexpected response: %s" % response)
        except HttpError, e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS, e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print error
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print "Sleeping %f seconds and then retrying..." % sleep_seconds
            time.sleep(sleep_seconds)
