#encoding: utf-8

import os
import subprocess
import shlex

from settings import dirname
from configuracion import config

_process_line = "* * * * * /usr/bin/env python %s procesar_video" % os.path.join(dirname, 'manage.py')
_publish_line = "* * * * * /usr/bin/env python %s publicar_video" % os.path.join(dirname, 'manage.py')

"""
Devuelve una lista donde cada elemento es una línea de crontab actual (puede contener comentarios).
"""
def _get_crontab():
    command = "%s -l" % config.get_option('CRONTAB_PATH')
    return subprocess.Popen(shlex.split(str(command)), stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()[0].strip().split('\n')

"""
Fija al crontab las líneas que componen la lista dada.
"""
def _set_crontab(data):
    command = "%s -" % config.get_option('CRONTAB_PATH')
    text = '\n'.join(data) + '\n'
    subprocess.Popen(shlex.split(str(command)), stdin = subprocess.PIPE).communicate(input = text)

"""
Devuelve si la tarea de procesamiento está activa en el crontab actual.
"""
def status(publish = False):
    cronline = _publish_line if publish else _process_line
    return cronline in _get_crontab()

"""
Elimina del crontab actual la tarea de procesamiento.
"""
def stop(publish = False):
    data = _get_crontab()
    cronline = _publish_line if publish else _process_line
    if cronline in data:
        data.remove(cronline)
    _set_crontab(data)

"""
Añade al crontab actual la tarea de procesamiento.
"""
def start(publish = False):
    data = _get_crontab()
    cronline = _publish_line if publish else _process_line
    if not cronline in data:
        data.append(cronline)
    _set_crontab(data)
