#encoding: utf-8

from postproduccion.models import Token
from postproduccion import utils
from configuracion import config

from datetime import datetime, timedelta

"""
Crea un nuevo token y devuelve su valor.
"""
def create_token(v):
    t = Token(video = v, token = utils.generate_token(128))
    t.save()
    return t.token

"""
Verifica que una petición es válida. En caso afirmativo devuelve el vídeo asociado.
"""
def is_valid_token(tk_str):
    tk_query = Token.objects.filter(token = tk_str, instante__gt = datetime.now() - timedelta(days = int(config.get_option('TOKEN_VALID_DAYS'))))
    if tk_query.count() != 1: return False
    return tk_query[0].video

"""
Borra los tokens caducados.
"""
def purge_expired_tokens():
    Token.objects.filter(instante__lt = datetime.now() - timedelta(days = int(config.get_option('TOKEN_VALID_DAYS')))).delete()

"""
Borra de la base de datos un token que ya ha sido atendido
"""
def token_attended(v):
    v.token.delete()
