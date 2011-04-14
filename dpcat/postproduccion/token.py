#encoding: utf-8

from django.shortcuts import render_to_response
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
Genera el mensaje de correo con las indicaciones para usar el token.
"""
def generate_mail_message(v):
    (nombre, titulo, vid, fecha) = (v.autor, v.titulo, v.id, v.informeproduccion.fecha_grabacion)
    url = urljoin(config.get_option('SITE_URL'), reverse('postproduccion.views.aprobacion_video', args=(v.token.token,))) 
    return render_to_response('postproduccion/mail_message.txt', { 
        'nombre' : nombre,
        'titulo' : titulo,
        'vid'    : vid,
        'fecha'  : fecha,
        'url'    : url,
        }).content
    

"""
Envía un correo al usuario para solicitar la aprobación y los metadatos de un vídeo.
"""
def send_mail_to_user(v):
    v = create_token(v)
    send_mail('UDV: Vídeo completado', generate_mail_message(v), 'pchinea@ull.es', [v.email])
    return v

