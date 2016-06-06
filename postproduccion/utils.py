# encoding: utf-8

import string
import random
import unicodedata
import os
import threading
import subprocess
import shlex
import re
import json

from django.conf import settings
from configuracion import config

"""
Declara un cerrojo global para los bloqueos entre threads.
"""
lock = threading.Lock()


def set_default_settings():
    """
    Fija los valores de configuración por defecto
    """
    defaults = [
        ['MAX_ENCODING_TASKS', 5],
        ['MELT_PATH', which('melt')],
        ['AVCONV_PATH', which('avconv')],
        ['MP4BOX_PATH', which('MP4Box')],
        ['CRONTAB_PATH', which('crontab')],
        ['MEDIAINFO_PATH', which('mediainfo')],
        ['EXIFTOOL_PATH', which('exiftool')],
        ['EXIFTOOL_CONFIG', os.path.join(
            settings.MEDIA_ROOT,
            'config/exiftool_dpcat.config'
        )],
        ['MAX_PREVIEW_WIDTH', 400],
        ['MAX_PREVIEW_HEIGHT', 300],
        ['VIDEO_LIBRARY_PATH', '/home/adminudv/videos/videoteca/'],
        ['VIDEO_INPUT_PATH', '/home/adminudv/videos/'],
        ['PREVIEWS_PATH', '/home/adminudv/videos/previews/'],
        ['TOKEN_VALID_DAYS', 7],
        ['SITE_URL', 'http://127.0.0.1:8000'],
        ['LOG_MAX_LINES', 1000],
        ['MAX_NUM_LOGFILES', 6],
        ['RETURN_EMAIL', 'noreply@dpcat.es'],
    ]

    for op in defaults:
        config.get_option(op[0]) or config.set_option(op[0], op[1])


def generate_token(length):
    """
    Genera un token alfanumérico del tamaño dado
    """
    random.seed()
    return "".join(
        [random.choice(string.letters + string.digits) for x in range(length)]
    )


def normalize_filename(name):
    """
    Normaliza una cadena para generar nombres de fichero seguros.
    """
    return unicodedata.normalize('NFKD', name).encode(
        'ascii',
        'ignore'
    ).translate(None, string.punctuation).replace(' ', '_')


def normalize_string(string):
    """
    Devuelve una cadena normalizada a partir de una de tipo unicode.
    """
    try:
        return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
    except:
        return string


def generate_safe_filename(name, date, extension):
    """
    Genera un nombre de fichero para un nuevo vídeo
    """
    day = date.strftime("%Y/%m/%d")
    safename = normalize_filename(name)
    return "%s_%s_%s%s" % (day, safename, generate_token(8), extension)


def ensure_dir(f):
    """
    Se asegura de que exista un directorio antes de crear un fichero en él.
    """
    d = os.path.dirname(f)
    lock.acquire()
    if not os.path.exists(d):
        os.makedirs(d)
    lock.release()


def remove_file_path(f):
    """
    Borra el fichero dado y los directorios que lo contienen si están vacíos.
    """
    if os.path.isfile(f):
        os.remove(f)
        try:
            os.removedirs(os.path.dirname(f))
        except OSError:
            pass


def is_dir(path):
    """
    Comprueba si la ruta dada coresponde a un directorio
    """
    return os.path.isdir(path)


def is_exec(fpath):
    """
    Comprueba si la ruta dada corresponde a un fichero ejecutable
    """
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def run_command(*commands):
    """
    Ejecutar comando con posibilidad de concatenar tuberías
    """
    p = subprocess.Popen(
        shlex.split(str(commands[0])),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    for cmd in commands[1:]:
        prev = p
        p = subprocess.Popen(
            shlex.split(str(cmd)),
            stdin=prev.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

    return p.communicate()[0]


def which(fpath):
    """
    Trata de localizar la ruta del ejecutable dado en el PATH
    """
    return run_command("/usr/bin/which %s" % fpath)


def avconv_version():
    """
    Devuelve la versión del avconv instalado.
    """
    fpath = config.get_option('AVCONV_PATH')
    if is_exec(fpath):
        data = run_command('%s -version' % fpath)
        try:
            return re.match('avconv version ([\.0-9]+)', data).group(1)
        except AttributeError:
            return None


def melt_version():
    """
    Devuelve la versión del melt instalado.
    """
    fpath = config.get_option('MELT_PATH')
    if is_exec(fpath):
        data = run_command('%s -version' % fpath)
        try:
            return re.search('melt ([\.0-9]+)', data).group(1)
        except AttributeError:
            return None


def mediainfo_version():
    """
    Devuelve la versión del mediainfo instalado.
    """
    fpath = config.get_option('MEDIAINFO_PATH')
    if is_exec(fpath):
        data = run_command('%s --Version' % fpath)
        try:
            return re.search('(v[0-9\.]+)$', data).group(1)
        except AttributeError:
            return None


def mp4box_version():
    """
    Devuelve la versión del MP4Box instalado.
    """
    fpath = config.get_option('MP4BOX_PATH')
    if is_exec(fpath):
        data = run_command('%s -version' % fpath)
        try:
            return re.search('version (\S*)', data).group(1)
        except AttributeError:
            return None


def exiftool_version():
    """
    Devuelve la versión del exiftool instalado.
    """
    fpath = config.get_option('EXIFTOOL_PATH')
    if is_exec(fpath):
        data = run_command('%s -ver' % fpath)
        try:
            return re.search('([\.0-9]+)', data).group(1)
        except AttributeError:
            return None


def df(fpath):
    """
    Devuelve la información de uso del sistema
    de ficheros en el que se encuentra la ruta dada.
    """
    data = run_command('df %s -Ph' % fpath).strip().splitlines()[1]
    return re.search('^.* +([\.0-9,]+[KMGTPEZY]?) +([\.0-9,]+[KMGTPEZY]?) +([\.0-9,]+[KMGTPEZY]?) +([\.0-9,]+%) +(/.*$)', data).group(1, 2, 3, 4, 5)


def dpcat_info():
    """
    Devuelve la información acerca de la versión actual de dpCat.
    """
    info = {}
    repo = 'https://github.com/tic-ull/dpCat/tree/'

    info['version'] = run_command('git tag', 'tail -1').strip()
    tag_version = run_command('git rev-list --count %s' %
                              info['version']).strip()
    head_version = run_command('git rev-list --count HEAD').strip()
    if tag_version != head_version:
        info['version'] = 'HEAD'
    info['commit'] = 'r.%s.%s' % (
        run_command('git rev-list --count %s' % info['version']).strip(),
        run_command('git rev-parse --short %s' % info['version']).strip()
    )
    info['branch'] = run_command(
        'git branch', 'grep *', 'cut -d " " -f2'
    ).strip()
    info['url'] = repo + run_command('git rev-parse %s' %
                                     info['version']).strip()
    info['date'] = run_command('git show -s --format=%%ci %s' %
                               info['version']).strip()
    info['message'] = run_command('git show -s --format=%%B %s' %
                                  info['version']).strip()
    info['author'] = run_command('git show -s --format=%%an %s' %
                                 info['version']).strip()

    return info


def check_dir(fpath):
    """
    Comprueba si el directorio dado existe y es accesible.
    Si no existe y puede, lo creará y devolverá verdadero.
    """
    if os.path.isdir(fpath) and os.access(fpath, os.R_OK | os.W_OK | os.X_OK):
        return True
    if not os.path.exists(fpath):
        try:
            os.makedirs(fpath)
        except:
            return False
        return True
    else:
        return False


def time_to_seconds(t):
    """
    Convierte, en caso necesario, una marca temporal
    en formato HH:MM:SS.ss a segundos.
    """
    try:
        return float(t)
    except ValueError:
        ct = t.split(':')
        return float(ct[0]) * 3600 + float(ct[1]) * 60 + float(ct[2])


class FileIterWrapper(object):
    """
    Clase envoltorio que permite iterar sobre un fichero.
    """
    def __init__(self, flo, chunk_size=1024**2):
        self.flo = flo
        self.chunk_size = chunk_size

    def next(self):
        data = self.flo.read(self.chunk_size)
        if data:
            return data
        else:
            raise StopIteration

    def __iter__(self):
        return self


def stream_file(filename):
    """
    Devuelve a modo de flujo el contenido del fichero dado.
    """
    return FileIterWrapper(open(filename, "rb"))
