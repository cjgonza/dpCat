#encoding: utf-8
from django.shortcuts import render_to_response
from postproduccion.encoder import get_mm_info, get_file_info, format_types, encode_mixed_video, encode_preview
from postproduccion.models import TecData
from configuracion import config

import os
import tempfile

"""
Renderiza el fichero de configuración del MELT para la codificación de una píldora
"""
def get_fdv_template(v):

    data = dict()

    data['plantilla'] = dict([
        ('fondo', v.plantilla.fondo.path),
        ('d_geom', "%d,%d:%dx%d:%d" % (
            v.plantilla.diapositiva_x,
            v.plantilla.diapositiva_y,
            v.plantilla.diapositiva_ancho,
            v.plantilla.diapositiva_alto,
            v.plantilla.diapositiva_mix,
        )),
        ('v_geom', "%d,%d:%dx%d:%d" % (
            v.plantilla.video_x,
            v.plantilla.video_y,
            v.plantilla.video_ancho,
            v.plantilla.video_alto,
            v.plantilla.video_mix,
        )),
    ])

    data['diapositiva'] = dict()
    data['presentador'] = dict()

    data['diapositiva']['fichero'] = v.ficheroentrada_set.filter(tipo=v.plantilla.diapositiva_tipo)[0].fichero
    data['presentador']['fichero'] = v.ficheroentrada_set.filter(tipo=v.plantilla.video_tipo)[0].fichero

    d_info = get_mm_info(data['diapositiva']['fichero'])
    p_info = get_mm_info(data['presentador']['fichero'])

    data['duracion'] = int(float(d_info['ID_LENGTH'] if d_info['ID_LENGTH'] < p_info['ID_LENGTH'] else p_info['ID_LENGTH'])) * 25

    data['diapositiva']['vcodec'] = format_types[d_info['ID_VIDEO_CODEC']]
    data['presentador']['vcodec'] = format_types[p_info['ID_VIDEO_CODEC']]
    data['presentador']['acodec'] = format_types[p_info['ID_AUDIO_CODEC']]

    return render_to_response('postproduccion/get_fdv_template.mlt', { 'data' : data })

"""

"""
def create_pil(video, logfile):
    # Guarda la plantilla en un fichero temporal
    (handler, path) = tempfile.mkstemp(suffix='.mlt')
    os.write(handler, get_fdv_template(video).content)
    os.close(handler)

    # Montaje y codificación de la píldora
    encode_mixed_video(path, video.fichero, logfile)

    # Obtiene la información técnica del vídeo generado.
    generate_tecdata(video)

    # Borra el fichero temporal
    os.unlink(path)

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


def create_preview(video, logfile):
    size = calculate_preview_size(video)
    filename = video.fichero
    outfile = "/tmp/loquesea.flv"

    encode_preview(filename, outfile, size, logfile)
