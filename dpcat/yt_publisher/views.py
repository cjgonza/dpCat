# Create your views here.
# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from oauth2client import xsrfutil

from yt_publisher.forms import ConfigForm
from yt_publisher.functions import Storage, get_flow
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
    return render_to_response("section-config-plugin.html", { 'form' : form, 'auth_state' : auth_state }, context_instance=RequestContext(request))


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
Callback para la autorización OAuth2 de YouTube.
"""
@permission_required('postproduccion.video_manager')
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], None):
        return  HttpResponseBadRequest()
    credentials = get_flow().step2_exchange(request.REQUEST)
    Storage().put(credentials)
    messages.success(request, u'Asociada cuenta de publicación')
    return HttpResponseRedirect(reverse("config_plugin"))

