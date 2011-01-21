#encoding: utf-8

import datetime
from settings import MEDIA_ROOT

"""
Constantes con los caracteres que representan el tipo de mensaje.
"""
INFO = 'I'
WARNING = 'W'
ERROR = 'E'

"""
Escribe un mensaje en el log de la aplicación
"""
def _print_log(status, msg):
    f = open(MEDIA_ROOT + '/logs/application.log', 'a')
    f.write("%c[%s] %s\n" % (status, datetime.datetime.now().__str__(), msg))
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
        ERROR   : "error"
    }
    return { 'status' : STATUS_TEXT[line[0]], 'msg' : line[1:].strip() }

"""
Devuelve una lista con todas las entradas del log
"""
def getlog():
    f = open(MEDIA_ROOT + '/logs/application.log', 'r')
    log = map(_parse_log_line, f.readlines())
    f.close()
    return log
