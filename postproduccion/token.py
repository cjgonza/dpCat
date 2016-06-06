# encoding: utf-8
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from postproduccion.models import Token, Video
from postproduccion import utils
from configuracion import config

from datetime import datetime, timedelta
from urlparse import urljoin


def create_token(v):
    """
    Crea un nuevo token y devuelve su valor.
    """
    if hasattr(v, 'token'): v.token.delete()
    t = Token(video=v, token=utils.generate_token(25))
    t.save()
    return Video.objects.get(token=t)


def is_valid_token(tk_str):
    """
    Verifica que una petición es válida.
    En caso afirmativo devuelve el vídeo asociado.
    """
    tk_query = Token.objects.filter(
        token=tk_str,
        instante__gt=datetime.now() - timedelta(
            days=int(config.get_option('TOKEN_VALID_DAYS'))
        )
    )
    if tk_query.count() != 1: return False
    return tk_query[0].video


def get_expired_tokens(days=None):
    """
    Devuelve los tokens caducados.
    """
    if days is None:
        return Token.objects.filter(
            id__gt=2179,
            instante__lt=datetime.now() - timedelta(
                days=int(config.get_option('TOKEN_VALID_DAYS'))
            )
        )
    else:
        return Token.objects.filter(
            id__gt=2179,
            instante__gt=datetime.today() - timedelta(days=days)
        )


def purge_expired_tokens():
    """
    Borra los tokens caducados.
    """
    get_expired_tokens().delete()


def get_token_data(v):
    """
    Devuelve un hash con los datos del token del vídeo o falso si no existe.
    """
    if hasattr(v, 'token'):
        return {
            'create_date': v.token.instante,
            'expiration_date': v.token.instante + timedelta(
                days=int(config.get_option('TOKEN_VALID_DAYS'))
            ),
            'valid': True if is_valid_token(v.token.token) else False,
            'url': get_token_url(v),
        }
    else:
        return False


def get_expire_time(t):
    """
    Devuelve la fecha de caducidad de un token.
    """
    return t.instante + timedelta(
        days=int(config.get_option('TOKEN_VALID_DAYS'))
    )


def token_attended(v):
    """
    Borra de la base de datos un token que ya ha sido atendido
    """
    v.token.delete()
    return Video.objects.get(id=v.id)


def get_token_url(v):
    """
    Devuelve la url del ticket de usuario correspondiente al vídeo dado.
    """
    return urljoin(
        config.get_option('SITE_URL'),
        reverse('postproduccion.views.aprobacion_video', args=(v.token.token,))
    )


def generate_mail_message(v):
    """
    Genera el mensaje de correo con las indicaciones para usar el token.
    """
    (nombre, titulo, vid, fecha) = (
        v.autor,
        v.titulo,
        v.id,
        v.informeproduccion.fecha_grabacion
    )
    url = get_token_url(v)
    return Template(config.get_option('NOTIFY_MAIL_MESSAGE')).render(Context({
        'nombre': nombre,
        'titulo': titulo,
        'vid': vid,
        'fecha': fecha,
        'url': url,
        'validez': get_token_data(v)['expiration_date'],
    }))


def send_mail_to_user(v):
    """
    Envía un correo al usuario para solicitar
    la aprobación y los metadatos de un vídeo.
    """
    v = create_token(v)
    try:
        send_mail(
            config.get_option('NOTIFY_MAIL_SUBJECT'),
            generate_mail_message(v),
            config.get_option('RETURN_EMAIL'),
            [v.email]
        )
    except:
        return None
    return v


def generate_custom_mail_message(v, texto, operador):
    """
    Genera el mensaje de correo personalizado
    con las indicaciones para usar el token.
    """
    (nombre, titulo, vid, fecha) = (
        v.autor,
        v.titulo,
        v.id,
        v.informeproduccion.fecha_grabacion
    )
    url = get_token_url(v)
    return Template(config.get_option('CUSTOM_MAIL_MESSAGE')).render(Context({
        'nombre': nombre,
        'titulo': titulo,
        'vid': vid,
        'fecha': fecha,
        'texto': texto,
        'url': url,
        'operador': operador,
        'validez': get_token_data(v)['expiration_date'],
        }))


def send_custom_mail_to_user(v, texto, operador):
    """
    Envía un correo personalizado al usuario
    para solicitar la aprobación y los metadatos de un vídeo.
    """
    v = create_token(v)
    try:
        send_mail(
            config.get_option('CUSTOM_MAIL_SUBJECT'),
            generate_custom_mail_message(v, texto, operador),
            config.get_option('RETURN_EMAIL'),
            [v.email]
        )
    except:
        return None
    return v


def generate_validation_mail_message(v, operador):
    """
    Genera el mensaje de correo para avisar al
    usuario de que su producción ya ha sido validada.
    """
    (nombre, titulo, vid, fecha) = (
        v.autor,
        v.titulo,
        v.id,
        v.informeproduccion.fecha_grabacion
    )
    return Template(config.get_option('VALIDATED_MAIL_MESSAGE')).render(
        Context({
            'nombre': nombre,
            'titulo': titulo,
            'vid': vid,
            'fecha': fecha,
            'operador': operador,
        })
    )


def send_validation_mail_to_user(v, operador):
    """
    Envía un correo para avisar al usuario de
    que su producción ya ha sido validada.
    """
    try:
        send_mail(
            config.get_option('VALIDATED_MAIL_SUBJECT'),
            generate_validation_mail_message(v, operador),
            config.get_option('RETURN_EMAIL'),
            [v.email]
        )
    except:
        return None
    return v


def generate_published_mail_message(r):
    """
    Genera el mensaje de correo para avisar al
    usuario de que su producción ya ha sido publicada.
    """
    (nombre, titulo, vid, fecha, url) = (
        r.video.autor,
        r.video.titulo,
        r.video.id,
        r.fecha,
        r.enlace
    )
    return Template(config.get_option('PUBLISHED_MAIL_MESSAGE')).render(
        Context({
            'nombre': nombre,
            'titulo': titulo,
            'vid': vid,
            'fecha': fecha,
            'url': url,
            })
    )


def send_published_mail_to_user(r):
    """
    Envía un correo para avisar al usuario
    de que su producción ya ha sido publicada.
    """
    try:
        send_mail(
            config.get_option('PUBLISHED_MAIL_SUBJECT'),
            generate_published_mail_message(r),
            config.get_option('RETURN_EMAIL'),
            [r.video.email]
        )
    except:
        return None
    return True
