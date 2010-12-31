#encoding: utf-8
from django.shortcuts import render_to_response
from postproduccion.encoder import get_mm_info, get_file_info, format_types, encode_mixed_video, encode_preview
from postproduccion.models import TecData, Previsualizacion
from configuracion import config
from postproduccion import utils

import os
import tempfile
import shutil

"""
Renderiza el fichero de configuración del MELT para la codificación de una píldora
"""
def get_fdv_template(v):
    data = dict()
    data['fondo'] = v.plantilla.fondo.path

    videos = list()
    duracion = list()
    for i in v.ficheroentrada_set.all():
        fe = dict()
        fe['fichero'] = i.fichero
        fe['geom'] = "%d,%d:%dx%d:%d" % (
            i.tipo.x,
            i.tipo.y,
            i.tipo.ancho,
            i.tipo.alto,
            i.tipo.mix
        )
        info = get_mm_info(i.fichero)
        fe['vcodec'] = format_types[info['ID_VIDEO_CODEC']]
        if 'ID_AUDIO_ID' in info:
            fe['acodec'] = format_types[info['ID_AUDIO_CODEC']]
        duracion.append(float(info['ID_LENGTH']))
        
        videos.append(fe)
    data['videos'] = videos
    data['duracion'] = int(min(duracion)) * 25

    return render_to_response('postproduccion/get_fdv_template.mlt', { 'data' : data })

"""
"""
def generate_tecdata(v):
    try:
        t = v.tecdata
    except TecData.DoesNotExist:
        t = TecData(video = v)
        t.save()

    for (key, value) in get_file_info(v.fichero).items():
        setattr(t, key, value)
    
    t.save()

def calculate_preview_size(v):
    width = float(v.tecdata.video_width)
    height = float(v.tecdata.video_height)
    ratio = float(v.tecdata.video_wh_ratio)
    max_width = float(config.get_option('MAX_PREVIEW_WIDTH'))
    max_height = float(config.get_option('MAX_PREVIEW_HEIGHT'))

    # Hace los pixels cuadrados
    if ratio > 0:
        width = height * ratio
    else:
        try:
            height = width / ratio
        except ZeroDivisionError:
            pass
    
    # Reduce el ancho
    if width > max_width:
        r = max_width / width
        width *= r
        height *= r

    # Reduce el alto
    if height > max_height:
        r = max_height / height
        width *= r
        height *= r

    # Hace el tamaño par (necesario para algunos codecs)
    width = int((width + 1) / 2) * 2
    height = int((height + 1) / 2) * 2

    return dict({'width' : width, 'height' : height, 'ratio' : ratio})

"""

"""
def create_pil(video, logfile):
    # Guarda la plantilla en un fichero temporal
    (handler, path) = tempfile.mkstemp(suffix='.mlt')
    os.write(handler, get_fdv_template(video).content)
    os.close(handler)

    # Genera el nombre del fichero de salida
    video.fichero = os.path.join(config.get_option('VIDEO_LIBRARY_PATH'), utils.generate_safe_filename(video.titulo, video.fecha_grabacion.date(), ".mp4"))
    video.save()

    # Montaje y codificación de la píldora
    utils.ensure_dir(video.fichero)
    encode_mixed_video(path, video.fichero, logfile)

    # Obtiene la información técnica del vídeo generado.
    generate_tecdata(video)

    # Borra el fichero temporal
    os.unlink(path)

def copy_video(video, logfile):
    # Obtiene los nombres de ficheros origen y destino
    src = video.ficheroentrada_set.all()[0].fichero
    dst = os.path.join(config.get_option('VIDEO_LIBRARY_PATH'), utils.generate_safe_filename(video.titulo, video.fecha_grabacion.date(), os.path.splitext(src)[1]))
    video.fichero = dst
    video.save()

    # Copia el fichero.
    utils.ensure_dir(video.fichero)
    shutil.copy(src, dst)
    os.write(logfile, '%s -> %s\n' % (src, dst))

    # Obtiene la información técnica del vídeo copiado.
    generate_tecdata(video)


def create_preview(video, logfile):
    # Obtiene los nombres de ficheros origen y destino
    src = video.fichero
    dst = os.path.join(config.get_option('PREVIEWS_PATH'), utils.generate_safe_filename(video.titulo, video.fecha_grabacion.date(), ".flv"))

    # Crea el objecto previsualización
    pv = Previsualizacion(video = video, fichero = dst)
    pv.save()

    # Calcula las dimensiones de la previsualización.
    size = calculate_preview_size(video)

    # Codifica la previsualización.
    utils.ensure_dir(pv.fichero)
    encode_preview(src, dst, size, logfile)
