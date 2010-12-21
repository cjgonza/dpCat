#encoding: utf-8

import string
import random
import unicodedata
import os
from datetime import date

from configuracion import config

"""
Fija los valores de configuración por defecto
"""
def set_defalut_settings():
    defaults = [
        [ 'MAX_ENCODING_TASKS', 5 ],
        [ 'MELT_PATH' ,         '/usr/bin/melt' ], 
        [ 'MPLAYER_PATH',       '/usr/bin/mplayer' ],
        [ 'FFMPEG_PATH',        '/usr/local/bin/ffmpeg' ],
        [ 'MAX_PREVIEW_WIDTH',  400 ],
        [ 'MAX_PREVIEW_HEIGHT', 300 ],
        [ 'VIDEO_LIBRARY_PATH', '/home/adminudv/videos/videoteca/'],
    ]

    for op in defaults:
        config.get_option(op[0]) or config.set_option(op[0], op[1])

"""
Genera un token alfanumérico del tamaño dado
"""
def generate_token(length):
    return "".join([random.choice(string.letters + string.digits) for x in range(length)])

"""
Genera un nombre de fichero para un nuevo vídeo
"""
def generate_safe_filename(name, extension):
    day = date.today().strftime("%Y/%m/%d")
    safename = unicodedata.normalize('NFKD', name).encode('ascii','ignore').translate(None, string.punctuation).replace(' ', '_')
    return "%s_%s_%s.%s" % (day, safename, generate_token(8), extension)

"""
Se asegura de que exista un directorio antes de crear un fichero en él.
"""
def ensure_dir(f):
    d = es.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
