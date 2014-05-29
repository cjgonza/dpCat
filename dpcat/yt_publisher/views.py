# Create your views here.
# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from oauth2client import xsrfutil

from postproduccion.models import Video
from yt_publisher.models import Publicacion
from yt_publisher.forms import ConfigForm, PublishingForm, AddToPlaylistForm, NewPlaylistForm
from yt_publisher.functions import Storage, Error
from yt_publisher.functions import get_flow, get_playlists, error_handler
from yt_publisher.functions import LICENSE_TEXTS
from configuracion import config
import settings

import json
import httplib2

"""
Edita los ajustes de configuración del plugin de publicación.
"""
@permission_required('postproduccion.video_manager')
def config_plugin(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            for i in form.base_fields.keys():
                config.set_option("YT_PUBLISHER_%s" % i.upper(), form.cleaned_data[i])
            messages.success(request, 'Configuración guardada')
    else:
        initial_data = dict()
        for i in ConfigForm.base_fields.keys():
            initial_data[i] = config.get_option("YT_PUBLISHER_%s" % i.upper())
        form = ConfigForm(initial = initial_data)
    auth_state = Storage().get() is not None
    return render_to_response("yt-section-config-plugin.html", { 'form' : form, 'auth_state' : auth_state }, context_instance=RequestContext(request))


"""
Gestiona la autorización y revocación de la cuenta de publicación.
"""
@permission_required('postproduccion.video_manager')
def auth_manage(request, revoke = False):
    credentials = Storage().get()
    if revoke:
        credentials.revoke(httplib2.Http())
        messages.warning(request, u'Eliminada cuenta de publicación')
    else:
        if credentials is None or credentials.invalid:
            flow = get_flow()
            flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, None)
            authorize_url = flow.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)

    return HttpResponseRedirect(reverse("config_plugin"))

"""
Realiza la publicación de la producción.
"""
@permission_required('postproduccion.video_manager')
def publicar(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        form = PublishingForm(request.POST)
        new_form = NewPlaylistForm(request.POST)
        add_form = AddToPlaylistForm(request.POST)
        try:
            add_form.fields['add_to_playlist'].choices = get_playlists()
        except Error as e:
            return error_handler(e, request)
        if form.is_valid() \
            and not (form.cleaned_data['playlist'] is 1 and not add_form.is_valid()) \
            and not (form.cleaned_data['playlist'] is 2 and not new_form.is_valid()):
            if form.cleaned_data['playlist'] is 0:
                pub_data = form.cleaned_data
            if form.cleaned_data['playlist'] is 1:
                pub_data = dict(form.cleaned_data, **add_form.cleaned_data)
            if form.cleaned_data['playlist'] is 2:
                pub_data = dict(form.cleaned_data, **new_form.cleaned_data)
            Publicacion(video = v, data = json.dumps(pub_data)).save()
            messages.success(request, u'Producción encolada para su publicación')
            return redirect('estado_video', v.id)
    else:
        form = PublishingForm()
        new_form = NewPlaylistForm()
        add_form = AddToPlaylistForm()
        metadataField = 'metadataoa' if v.objecto_aprendizaje else 'metadatagen'
        form.fields['title'].initial = getattr(v, metadataField).title
        form.fields['description'].initial = "%s\n\n---\n%s" % (getattr(v, metadataField).description, LICENSE_TEXTS[getattr(v, metadataField).license])
        form.fields['tags'].initial = "%s,%s" % (getattr(v, metadataField).keyword, getattr(v, metadataField).get_knowledge_areas_display().replace(',',''))
        try:
            add_form.fields['add_to_playlist'].choices = get_playlists()
        except Error as e:
            return error_handler(e, request)

    return render_to_response("yt-section-publish.html", { 'form' : form, 'new_form' : new_form, 'add_form' : add_form }, context_instance=RequestContext(request))

"""
Callback para la autorización OAuth2 de YouTube.
"""
@permission_required('postproduccion.video_manager')
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], None):
        return  HttpResponseBadRequest()
    try:
        credentials = get_flow().step2_exchange(request.REQUEST)
        Storage().put(credentials)
        messages.success(request, u'Asociada cuenta de publicación')
    except Error:
        messages.error(request, u'Autorización no concedida')
    return HttpResponseRedirect(reverse("config_plugin"))

@permission_required('postproduccion.video_manager')
def test(request):
    try:
        lista = get_playlists()
    except Error as e:
        return error_handler(e, request)

    return HttpResponse(lista)

"""
Muestra la cola de publicación.
"""
@permission_required('postproduccion.video_manager')
def cola_publicacion(request):
    return render_to_response("yt-section-cola.html", context_instance=RequestContext(request))

"""
Contenido de la cola de publicación.
"""
@permission_required('postproduccion.video_manager')
def contenido_cola_publicacion(request):
    return render_to_response("yt-ajax-cola.html", { 'list' : Publicacion.objects.order_by('id') }, context_instance=RequestContext(request))

"""
Purga las publicaciones erroneas
"""
@permission_required('postproduccion.video_manager')
def purgar_publicaciones(request):
    failed = Publicacion.objects.get_failed()
    cont = failed.count()
    failed.delete()
    messages.success(request, u'Publicaciones erroneas purgadas. Nº de elementos borrados: %d' % cont)
    return redirect('cola_publicacion')
