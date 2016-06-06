# encoding: utf-8

import os
import subprocess
import shlex

from django.conf import settings
from configuracion import config

_cronline = "* * * * * /usr/bin/env python %s" % os.path.join(
    settings.BASE_DIR,
    'manage.py'
)


def _get_crontab():
    """
    Devuelve una lista donde cada elemento es una línea
    de crontab actual (puede contener comentarios).
    """
    command = "%s -l" % config.get_option('CRONTAB_PATH')
    return subprocess.Popen(
        shlex.split(str(command)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()[0].strip().split('\n')


def _set_crontab(data):
    """
    Fija al crontab las líneas que componen la lista dada.
    """
    command = "%s -" % config.get_option('CRONTAB_PATH')
    text = '\n'.join(data) + '\n'
    subprocess.Popen(
        shlex.split(str(command)),
        stdin=subprocess.PIPE
    ).communicate(input=text)


def status(command):
    """
    Devuelve si la tarea de procesamiento está activa en el crontab actual.
    """
    cronline = "%s %s" % (_cronline, command)
    return cronline in _get_crontab()


def stop(command):
    """
    Elimina del crontab actual la tarea de procesamiento.
    """
    data = _get_crontab()
    cronline = "%s %s" % (_cronline, command)
    if cronline in data:
        data.remove(cronline)
    _set_crontab(data)


def start(command):
    """
    Añade al crontab actual la tarea de procesamiento.
    """
    data = _get_crontab()
    cronline = "%s %s" % (_cronline, command)
    if cronline not in data:
        data.append(cronline)
    _set_crontab(data)
