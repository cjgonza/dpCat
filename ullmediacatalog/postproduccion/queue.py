#encoding: utf-8
from postproduccion.models import Cola
from postproduccion.video import create_pil, create_preview, copy_video
from settings import MEDIA_ROOT

import os
import re
import tempfile
from datetime import datetime

"""
Encola el video de tipo normal dado para que sea copiado.
"""
def enqueue_copy(video_id):
    c = Cola(video=video_id, tipo='COP')
    c.save()

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

    if task.tipo == 'COP':
        copy_video(task.video, handle)
        enqueue_preview(task.video)
    if task.tipo == 'PIL':
        create_pil(task.video, handle)
        enqueue_preview(task.video)
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

    if task.tipo == 'COP':
        src = task.video.ficheroentrada_set.all()[0].fichero
        dst = task.video.fichero
        try:
            src_size = os.stat(src).st_size
            dst_size = os.stat(dst).st_size
            return int(float(dst_size) * 100 / float(src_size))
        except:
            return 0

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

    if pro < 0 or pro > 100:
        pro = 0

    os.close(fd)

    return pro

"""
Elimina de la lista los trabajos completados.
"""
def removeCompleted():
    Cola.objects.filter(status='HEC').delete()
