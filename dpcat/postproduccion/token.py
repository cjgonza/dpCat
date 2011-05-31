#encoding: utf-8
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from postproduccion.models import Token, Video
from postproduccion import utils
from configuracion import config

from datetime import datetime, timedelta
from urlparse import urljoin

"""
Crea un nuevo token y devuelve su valor.
"""
def create_token(v):
    if hasattr(v, 'token'): v.token.delete()
    t = Token(video = v, token = utils.generate_token(25))
    t.save()
    return Video.objects.get(token = t)

"""
Verifica que una petición es válida. En caso afirmativo devuelve el vídeo asociado.
"""
def is_valid_token(tk_str):
    tk_query = Token.objects.filter(token = tk_str, instante__gt = datetime.now() - timedelta(days = int(config.get_option('TOKEN_VALID_DAYS'))))
    if tk_query.count() != 1: return False
    return tk_query[0].video

"""
Devuelve los tokens caducados.
"""
def get_expired_tokens():
    return Token.objects.filter(instante__lt = datetime.now() - timedelta(days = int(config.get_option('TOKEN_VALID_DAYS'))))

"""
Borra los tokens caducados.
"""
def purge_expired_tokens():
    get_expired_tokens().delete()

"""
Devuelve un hash con los datos del token del vídeo o falso si no existe.
"""
def get_token_data(v):
    if hasattr(v, 'token'):
        return {
            'create_date' : v.token.instante,
            'expiration_date' : v.token.instante + timedelta(days = int(config.get_option('TOKEN_VALID_DAYS'))),
            'valid' : True if is_valid_token(v.token.token) else False,
            'url' : get_token_url(v),
        }
    else:
        return False

"""
Devuelve la fecha de caducidad de un token.
"""
def get_expire_time(t):
    return t.instante + timedelta(days = int(config.get_option('TOKEN_VALID_DAYS')))

"""
Borra de la base de datos un token que ya ha sido atendido
"""
def token_attended(v):
    v.token.delete()
    return Video.objects.get(id = v.id)

"""
Devuelve la url del ticket de usuario correspondiente al vídeo dado.
"""
def get_token_url(v):
    return urljoin(config.get_option('SITE_URL'), reverse('postproduccion.views.aprobacion_video', args=(v.token.token,))) 


"""
Genera el mensaje de correo con las indicaciones para usar el token.
"""
def generate_mail_message(v):
    (nombre, titulo, vid, fecha) = (v.autor, v.titulo, v.id, v.informeproduccion.fecha_grabacion)
    url = get_token_url(v)
    return render_to_string('postproduccion/mail-validar-message.txt', { 
        'nombre' : nombre,
        'titulo' : titulo,
        'vid'    : vid,
        'fecha'  : fecha,
        'url'    : url,
        })

"""
Envía un correo al usuario para solicitar la aprobación y los metadatos de un vídeo.
"""
def send_mail_to_user(v):
    v = create_token(v)
    send_mail('dpCat: Vídeo completado', generate_mail_message(v), None, [v.email])
    return v

"""
Genera el mensaje de correo personalizado con las indicaciones para usar el token.
"""
def generate_custom_mail_message(v, texto, operador):
    (nombre, titulo, vid, fecha) = (v.autor, v.titulo, v.id, v.informeproduccion.fecha_grabacion)
    url = get_token_url(v)
    return render_to_string('postproduccion/mail-custom-message.txt', {
        'nombre'   : nombre,
        'titulo'   : titulo,
        'vid'      : vid,
        'fecha'    : fecha,
        'texto'    : texto,
        'url'      : url,
        'operador' : operador,
        })

"""
Envía un correo personalizado al usuario para solicitar la aprobación y los metadatos de un vídeo.
"""
def send_custom_mail_to_user(v, texto, operador):
    v = create_token(v)
    send_mail('dpCat: Comentario del operador', generate_custom_mail_message(v, texto, operador), None, [v.email])
    return v

"""
Genera el mensaje de correo para avisar al usuario de que su producción ya ha sido validada.
"""
def generate_validation_mail_message(v, operador):
    (nombre, titulo, vid, fecha) = (v.autor, v.titulo, v.id, v.informeproduccion.fecha_grabacion)
    return render_to_string('postproduccion/mail-validada-message.txt', { 
        'nombre'   : nombre,
        'titulo'   : titulo,
        'vid'      : vid,
        'fecha'    : fecha,
        'operador' : operador,
        })

"""
Envía un correo para avisar al usuario de que su producción ya ha sido validada.
"""
def send_validation_mail_to_user(v, operador):
    send_mail('dpCat: Producción validada', generate_validation_mail_message(v, operador), None, [v.email])
    return v
