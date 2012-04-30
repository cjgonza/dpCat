# Create your views here.
# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from cb_publisher.models import Publicacion
from cb_publisher.forms import ConfigForm, PublishingForm
from cb_publisher.functions import get_categories
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
    return render_to_response("postproduccion/section-config.html", { 'form' : form }, context_instance=RequestContext(request))

"""
Realiza la publicación de la producción.
"""
@permission_required('postproduccion.video_manager')
def publicar(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        form = PublishingForm(request.POST)
        form.fields['category'].choices = get_categories()
        if form.is_valid():
            Publicacion(video = v, data = json.dumps(form.cleaned_data)).save()
            messages.success(request, u'Producción encolada para su publicación')
            return redirect('estado_video', v.id)
    else:
        form = PublishingForm()
        form.fields['title'].initial = v.metadata.title
        form.fields['description'].initial = v.metadata.description
        form.fields['tags'].initial = v.metadata.keyword
        form.fields['license'].initial = v.metadata.license
        form.fields['category'].choices = get_categories()
    return render_to_response("postproduccion/section-config.html", { 'form' : form }, context_instance=RequestContext(request))
