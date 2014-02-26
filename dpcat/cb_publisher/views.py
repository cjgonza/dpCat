# Create your views here.
# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from cb_publisher.models import Publicacion, RegistroPublicacionCB
from cb_publisher.forms import ConfigForm, PublishingForm, NewCollectionForm, AddToCollectionForm
from cb_publisher.functions import get_categories, send_published_mail_to_user, get_category_id, get_collection_categories, get_collections
from configuracion import config
from postproduccion.models import Video

import json

"""
Edita los ajustes de configuración del plugin de publicación.
"""
@permission_required('postproduccion.video_manager')
def config_plugin(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            for i in form.base_fields.keys():
                config.set_option("CB_PUBLISHER_%s" % i.upper(), form.cleaned_data[i])
            messages.success(request, 'Configuración guardada')
    else:
        initial_data = dict()
        for i in ConfigForm.base_fields.keys():
            initial_data[i] = config.get_option("CB_PUBLISHER_%s" % i.upper())
        form = ConfigForm(initial = initial_data)
    return render_to_response("cb_publisher/section-config.html", { 'form' : form }, context_instance=RequestContext(request))

"""
Realiza la publicación de la producción.
"""
@permission_required('postproduccion.video_manager')
def publicar(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        form = PublishingForm(request.POST)
        new_form = NewCollectionForm(request.POST)
        add_form = AddToCollectionForm(request.POST)
        form.fields['category'].choices = get_categories()
        new_form.fields['new_collection_category'].choices = get_collection_categories()
        add_form.fields['add_to_collection'].choices = get_collections()
        if form.is_valid() \
            and not (form.cleaned_data['collection'] is 1 and not add_form.is_valid()) \
            and not (form.cleaned_data['collection'] is 2 and not new_form.is_valid()):
            if form.cleaned_data['collection'] is 0:
                pub_data = form.cleaned_data
            if form.cleaned_data['collection'] is 1:
                pub_data = dict(form.cleaned_data, **add_form.cleaned_data)
            if form.cleaned_data['collection'] is 2:
                pub_data = dict(form.cleaned_data, **new_form.cleaned_data)
            print pub_data
            Publicacion(video = v, data = json.dumps(pub_data)).save()
            messages.success(request, u'Producción encolada para su publicación')
            return redirect('estado_video', v.id)
    else:
        form = PublishingForm()
        new_form = NewCollectionForm()
        add_form = AddToCollectionForm()
        metadataField = 'metadataoa' if v.objecto_aprendizaje else 'metadatagen'
        form.fields['title'].initial = getattr(v, metadataField).title
        form.fields['description'].initial = getattr(v, metadataField).description
        form.fields['tags'].initial = getattr(v, metadataField).keyword
        form.fields['license'].initial = getattr(v, metadataField).license
        try:
            form.fields['category'].choices = get_categories()
            form.fields['category'].initial = get_category_id(getattr(v, metadataField).get_knowledge_areas_display())
            new_form.fields['new_collection_category'].choices = get_collection_categories()
            add_form.fields['add_to_collection'].choices = get_collections()
        except IOError:
            messages.error(request, u'Imposible conectar con el servidor de publicación.')
            return redirect('estado_video', v.id)

    return render_to_response("cb_publisher/section-publish.html", { 'form' : form, 'new_form' : new_form, 'add_form' : add_form }, context_instance=RequestContext(request))

"""
Muestra la cola de publicación.
"""
@permission_required('postproduccion.video_manager')
def cola_publicacion(request):
    return render_to_response("cb_publisher/section-cola.html", context_instance=RequestContext(request))

"""
Contenido de la cola de publicación.
"""
@permission_required('postproduccion.video_manager')
def contenido_cola_publicacion(request):
    return render_to_response("cb_publisher/ajax-cola.html", { 'list' : Publicacion.objects.order_by('id') }, context_instance=RequestContext(request))

"""
Borra el registro dado
"""
@permission_required('postproduccion.video_manager')
def borrar_registro(request, record_id):
    r = get_object_or_404(RegistroPublicacionCB, pk = record_id)
    v = r.video
    r.delete()
    messages.success(request, u'Registro de publicación eliminado')
    return redirect('estado_video', v.id)

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

"""
Envía un correo al autor notificando de que una producción se encuentra publicada.
"""
@permission_required('postproduccion.video_manager')
def notificar_publicacion(request, record_id):
    r = get_object_or_404(RegistroPublicacionCB, pk = record_id)
    send_published_mail_to_user(r)
    messages.success(request, u'Enviado correo de notificación de publicacion al autor')
    return redirect('estado_video', r.video.id)
