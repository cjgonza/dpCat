#encoding: utf-8
from postproduccion.models import Cola
from postproduccion.video import encode_pil
from settings import MEDIA_ROOT

import os
import tempfile
from datetime import datetime

"""
Encola el video de tipo píldora dado para que sea montado.
"""
def enqueue_pil(video_id):
    c = Cola(video=video_id, tipo='PIL')
    c.save()

"""
Procesa el elemento dado de la cola.
"""
def process_task(task):

    # Crea el fichero para el registro de la salida de codificación.
    (handle, path) = tempfile.mkstemp(suffix = '.log', dir = MEDIA_ROOT + '/logs')

    # Actualiza la información de la base de datos.
    task.logfile = os.path.basename(path)
    task.comienzo = datetime.now()
    task.status = 'PRO'
    task.save()

    if task.tipo == 'PIL':
        encode_pil(task.video, handle)

    # Cierra el fichero de registro
    os.close(handle)
    
    # Actualiza la información de la base de datos.
    task.fin = datetime.now()
    task.status = 'HEC'
    task.save()

