#encoding: utf-8

import datetime
import gzip
import os
from settings import MEDIA_ROOT
from configuracion import config
from postproduccion.utils import lock

"""
Constantes con los caracteres que representan el tipo de mensaje.
"""
INFO = 'I'
WARNING = 'W'
ERROR = 'E'
DEBUG = 'D'

"""
Constante con el nombre de fichero del registro.
"""
LOGFILE = MEDIA_ROOT + '/logs/application.log'

"""
Escribe un mensaje en el log de la aplicación
"""
def _print_log(status, msg):
    _register_entry()
    f = open(LOGFILE, 'a')
    f.write("%c[%s] %s\n" % (status, datetime.datetime.now(), msg))
    f.close()

#
# Registro de procesos.
#

"""
Registra el encolado de una píldora.
"""
def pil_enqueue(v):
    _print_log(INFO, "Se encola la píldora '%s' para ser montada" % v)

"""
Registra el comienzo del montaje de una píldora.
"""
def pil_start(v):
    _print_log(INFO, "Comienza a montar la píldora '%s'" % v)

"""
Registra el final del montaje de una píldora.
"""
def pil_finish(v):
    _print_log(INFO, "Termina de montar la píldora '%s'" %  v)

"""
Registra un error en el montaje de una pídlora.
"""
def pil_error(v):
    _print_log(ERROR, "Error al montar la píldora '%s'" % v)

"""
Registra el encolado de la copia de un vídeo.
"""
def copy_enqueue(v):
    _print_log(INFO, "Se encola el vídeo '%s' para ser copiado" % v)

"""
Registra el comienzo del copiado de un vídeo.
"""
def copy_start(v):
    _print_log(INFO, "Comienza a copiar el vídeo '%s'" % v)

"""
Registra el final del copiado de un vídeo.
"""
def copy_finish(v):
    _print_log(INFO, "Termina de copiar el vídeo '%s'" % v)
    
"""
Registra un error en el copiado de un vídeo.
"""
def copy_error(v):
    _print_log(ERROR, "Error al copiar el vídeo '%s'" % v)
    
"""
Registra el encolado de una previsualización.
"""
def preview_enqueue(v):
    _print_log(INFO, "Se encola la previsualización de '%s' para ser codificada" % v)

"""
Registra el comienzo de la codificación de una previsualización.
"""
def preview_start(v):
    _print_log(INFO, "Comienza la previsualización de '%s'" % v)

"""
Registra el final de la codificación de una previsualización.
"""
def preview_finish(v):
    _print_log(INFO, "Termina la previsualización de '%s'" % v)
    
"""
Registra un error en la codificación de una previsualización.
"""
def preview_error(v):
    _print_log(ERROR, "Error con la previsualización de '%s'" % v)

#
# Manejo del registro
#

"""
Parsea una línea del log y devuelve un hash con el status y el mensaje.
"""
def _parse_log_line(line):
    STATUS_TEXT = {
        INFO    : "info",
        WARNING : "warning",
        ERROR   : "error",
        DEBUG   : "debug"
    }
    return { 'status' : STATUS_TEXT[line[0]], 'msg' : line[1:].strip() }

"""
Devuelve una lista con todas las entradas del fichero de log dado
"""
def _get_logfile(fname):
    f = open(fname, 'r')
    log = map(_parse_log_line, f.readlines())
    f.close()
    return log

"""
Devuelve una lista con todas las entradas del log
"""
def get_log():
    return _get_logfile(LOGFILE)

"""
Devuelve una lista con todas las entradas del log antiguo
"""
def get_old_log():
    return _get_logfile("%s.%s" % (LOGFILE, 1))


#
# Rotación del registro
#

"""
Comprime a gzip el fichero dado (borrando el original).
"""
def _compress_file(fname):
    f_in = open(fname, 'rb')
    f_out = gzip.open("%s.gz" % fname, 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    os.unlink(fname)

"""
Rota los registros comprimiendo los más antiguos.
"""
def _logrotate():
    for i in range(int(config.get_option('MAX_NUM_LOGFILES')) - 1, 1, -1):
        if os.path.isfile('%s.%s.gz' % (LOGFILE, i)):
            os.rename('%s.%s.gz' % (LOGFILE, i), '%s.%s.gz' % (LOGFILE, i + 1))
    if os.path.isfile('%s.%s' % (LOGFILE, 1)):
        os.rename('%s.%s' % (LOGFILE, 1), '%s.%s' % (LOGFILE, 2))
        _compress_file('%s.%s' % (LOGFILE, 2))
    if os.path.isfile(LOGFILE):
        os.rename(LOGFILE, '%s.%s' % (LOGFILE, 1))
    open(LOGFILE, 'w').close()

"""
Contabiliza una entrada en el registro y realiza la rotación en caso necesario.
"""
def _register_entry():
    lock.acquire()
    current = int(config.get_option('CURRENT_LOG_SIZE')) if config.get_option('CURRENT_LOG_SIZE') else 0
    if current >= int(config.get_option('LOG_MAX_LINES')):
        _logrotate()
        current = 1
    else:
        current += 1
    config.set_option('CURRENT_LOG_SIZE', current)
    lock.release()

