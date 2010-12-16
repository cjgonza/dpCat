#encoding: utf-8
from postproduccion.models import Cola
from postproduccion.video import create_pil, create_preview
from settings import MEDIA_ROOT

import os
import re
import tempfile
from datetime import datetime

"""
Encola el video de tipo píldora dado para que sea montado.
"""
def enqueue_pil(video_id):
    c = Cola(video=video_id, tipo='PIL')
    c.save()

"""
Encola un vídeo para generar su previsualización.
"""
def enqueue_preview(video_id):
    c = Cola(video=video_id, tipo='PRE')
    c.save()

"""
Procesa el elemento dado de la cola.
"""
def process_task(task):

    # Crea el fichero para el registro de la salida de codificación.
    (handle, path) = tempfile.mkstemp(suffix = '.log', dir = MEDIA_ROOT + '/logs')

    # Actualiza la información de la base de datos.
    task.logfile = 'logs/' + os.path.basename(path)
    task.comienzo = datetime.now()
    task.status = 'PRO'
    task.save()

    if task.tipo == 'PIL':
        create_pil(task.video, handle)
    if task.tipo == 'PRE':
        create_preview(task.video, handle)

    # Cierra el fichero de registro
    os.close(handle)
    
    # Actualiza la información de la base de datos.
    task.fin = datetime.now()
    task.status = 'HEC'
    task.save()

"""
Devuelve el progreso de codificación de una tarea.
"""
def progress(task):
    if task.status == 'PEN':
        return 0
    if task.status == 'HEC':
        return 100

    fd = os.open(task.logfile.path, os.O_RDONLY)
    try:
        os.lseek(fd, -255, os.SEEK_END)
        data = os.read(fd, 255)
        if task.tipo == 'PIL':
            pro = int(re.sub('.*percentage: *','',data).split(' ')[0])
        if task.tipo == 'PRE':
            pro = int(float(re.sub('.*time=','',data).split(' ')[0]) * 100 / task.video.tecdata.duration)
    except:
        pro = 0

    os.close(fd)

    return pro
