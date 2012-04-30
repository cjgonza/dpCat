# Create your views here.
# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from cb_publisher.forms import ConfigForm, PublishingForm
from configuracion import config
from postproduccion.models import Video


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
        """
        form = plugin.PublishingForm(request.POST)
        if form.is_valid():
            msg = plugin.publish(v, form.cleaned_data['category'])
            if msg == None:
                messages.success(request, u'Producción publicada')
            else:
                messages.error(request, u'Error publicando la producción:\n%s' % msg)
            return redirect('estado_video', v.id)
        """
        pass
    else:
        form = PublishingForm()
        form.fields['title'].initial = v.metadata.title
        form.fields['description'].initial = v.metadata.description
        form.fields['tags'].initial = v.metadata.keyword
    return render_to_response("postproduccion/section-config.html", { 'form' : form }, context_instance=RequestContext(request))
