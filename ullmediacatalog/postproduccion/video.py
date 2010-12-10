#encoding: utf-8
from django.shortcuts import render_to_response
from postproduccion.encoder import get_mm_info, get_file_info, format_types, encode_mixed_video

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
def encode_pil(video, logfile):
    # Guarda la plantilla en un fichero temporal
    (handler, path) = tempfile.mkstemp(suffix='.mlt')
    os.write(handler, get_fdv_template(video).content)
    os.close(handler)

    # Montaje y codificación de la píldora
    encode_mixed_video(path, video.fichero, logfile)

    # Borra el fichero temporal
    os.unlink(path)

"""
"""
def generate_tecdata(v):
    if not v.tecdata:
        v.tecdata = TecData()

    for (key, value) in get_file_data(v.fichero).items():
        setattr(v.tecdata, key, value)
    
    v.save()
