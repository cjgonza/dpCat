# Create your views here.
# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from postproduccion.models import Video, Cola, FicheroEntrada
from postproduccion.forms import VideoForm, FicheroEntradaForm, RequiredBaseInlineFormSet, MetadataForm, InformeCreacionForm, InformeRechazoForm
from postproduccion.queue import enqueue_copy, enqueue_pil, progress, get_log
from postproduccion import utils
from postproduccion import token
from postproduccion import log
from configuracion import config

import os
import urllib
import datetime

from django.contrib.auth.decorators import permission_required

"""
Muestra la página inicial
"""
@permission_required('postproduccion.video_manager')
def index(request):
    return render_to_response("postproduccion/inicio.html", { }, context_instance=RequestContext(request))


"""
Muestra el formulario para insertar un nuevo proyecto de vídeo.
"""
@permission_required('postproduccion.video_manager')
def crear(request, video_id = None):
    v = get_object_or_404(Video, pk=video_id) if video_id else None
    if request.method == 'POST':
        vform = VideoForm(request.POST, instance = v) if v else VideoForm(request.POST)
        iform = InformeCreacionForm(request.POST, instance = v.informeproduccion) if v else InformeCreacionForm(request.POST)
        if vform.is_valid():
            v = vform.save()
            i = iform.save(commit = False)
            i.video = v
            i.operador = request.user
            i.save()
            return HttpResponseRedirect(reverse('postproduccion.views.fichero_entrada', args=(v.id,)))
    else:
        vform = VideoForm(instance = v) if v else VideoForm()
        iform = InformeCreacionForm(instance = v.informeproduccion) if v else InformeCreacionForm()
    return render_to_response("postproduccion/crear.html", { 'vform' : vform, 'iform' : iform }, context_instance=RequestContext(request))


"""
Muestra el formulario para seleccionar el fichero de entrada.
"""
@permission_required('postproduccion.video_manager')
def _fichero_entrada_simple(request, v):
    if request.method == 'POST':
        form = FicheroEntradaForm(request.POST, instance = v.ficheroentrada_set.all()[0]) if v.ficheroentrada_set.count() else FicheroEntradaForm(request.POST)
        if form.is_valid():
            fe = form.save(commit = False)
            fe.video = v
            fe.fichero = os.path.normpath(config.get_option('VIDEO_INPUT_PATH') + fe.fichero)
            fe.save()
            return HttpResponseRedirect(reverse('postproduccion.views.resumen_video', args=(v.id,)))
    else:
        if  v.ficheroentrada_set.count():
            fe = v.ficheroentrada_set.all()[0]
            fe.fichero = os.path.join('/', os.path.relpath(fe.fichero, config.get_option('VIDEO_INPUT_PATH')))
            form = FicheroEntradaForm(instance = fe)
        else:
            form = FicheroEntradaForm()
    return render_to_response("postproduccion/fichero_entrada.html", { 'v' : v, 'form' : form }, context_instance=RequestContext(request))

"""
Muestra el formulario para seleccionar los ficheros de entrada.
"""
@permission_required('postproduccion.video_manager')
def _fichero_entrada_multiple(request, v):
    n = v.plantilla.tipovideo_set.count()
    FicheroEntradaFormSet = inlineformset_factory(Video, FicheroEntrada, formset = RequiredBaseInlineFormSet, extra = n, max_num = n, can_delete = False)
    tipos = v.plantilla.tipovideo_set.all().order_by('id')
    if request.method == 'POST':
        formset = FicheroEntradaFormSet(request.POST, instance = v)
        if formset.is_valid():
            instances = formset.save(commit = False)
            for i in range(n):
                instances[i].fichero = os.path.normpath(config.get_option('VIDEO_INPUT_PATH') + instances[i].fichero)
                instances[i].video = v
                instances[i].tipo = tipos[i]
                instances[i].save()
            return HttpResponseRedirect(reverse('postproduccion.views.resumen_video', args=(v.id,)))
    else:
        formset = FicheroEntradaFormSet(instance = v)
    
    for i in range(n):
        formset.forms[i].titulo = tipos[i].nombre
        if formset.forms[i].initial:
            formset.forms[i].initial['fichero'] = os.path.join('/', os.path.relpath(formset.forms[i].initial['fichero'], config.get_option('VIDEO_INPUT_PATH')))
    return render_to_response("postproduccion/ficheros_entrada.html", { 'v' : v, 'formset' : formset }, context_instance=RequestContext(request))

"""
Llama al método privado adecuado para insertar los ficheros de entrada según
el tipo de vídeo.
"""
@permission_required('postproduccion.video_manager')
def fichero_entrada(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if v.plantilla:
        return _fichero_entrada_multiple(request, v)
    else:
        return _fichero_entrada_simple(request, v)

"""
Muestra un resumen del vídeo creado.
"""
@permission_required('postproduccion.video_manager')
def resumen_video(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        if v.plantilla:
            enqueue_pil(v)
        else:
            enqueue_copy(v)
        v.set_status('DEF')
        return HttpResponseRedirect(reverse('postproduccion.views.index'))
    return render_to_response("postproduccion/resumen_video.html", { 'v' : v }, context_instance=RequestContext(request))

"""
Devuelve una lista (html) con el contenido de un directorio para usar con la
llamada AJAX del jqueryFileTree.
"""
@permission_required('postproduccion.video_manager')
@csrf_exempt
def dirlist(request):
    r=['<ul class="jqueryFileTree" style="display: none;">']
    try:
        r=['<ul class="jqueryFileTree" style="display: none;">']
        basedir = urllib.unquote(config.get_option('VIDEO_INPUT_PATH'))
        reqdir = urllib.unquote(request.POST.get('dir'))
        fulldir = os.path.normpath(basedir + reqdir)
        for f in os.listdir(fulldir):
            ff = os.path.join(reqdir, f)
            if os.path.isdir(os.path.join(fulldir, f)):
                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff, f))
            else:
                e =os.path.splitext(f)[1][1:] # get .ext and remove dot
                r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e, ff, f))
        r.append('</ul>')
    except Exception,e:
        r.append('Could not load directory: %s' % str(e))
    r.append('</ul>')
    return HttpResponse(''.join(r))

@permission_required('postproduccion.video_manager')
def cola_base(request):
    return render_to_response("postproduccion/cola_base.html", context_instance=RequestContext(request))

@permission_required('postproduccion.video_manager')
def cola_listado(request):
    import json
    data = list()
    for task in Cola.objects.order_by('pk'):
        linea = dict()
        linea['video'] = task.video.titulo
        linea['tipo'] = dict(Cola.QUEUE_TYPE)[task.tipo]
        linea['comienzo'] = task.comienzo.strftime("%d/%m/%Y %H:%M:%S.%f") if task.comienzo else None
        linea['fin'] = task.fin.strftime("%d/%m/%Y %H:%M:%S.%f") if task.fin else None
        linea['logfile'] = task.logfile.name
        linea['logurl'] = reverse('postproduccion.views.mostrar_log', args=(task.pk,)) if task.logfile.name else None
        linea['id'] = task.pk
        linea['status'] = progress(task) if task.status == 'PRO' else dict(Cola.QUEUE_STATUS)[task.status]
        data.append(linea)
    return HttpResponse(json.dumps(data))

"""
Muestra el fichero de log para una tarea.
"""
@permission_required('postproduccion.video_manager')
def mostrar_log(request, task_id):
    task = get_object_or_404(Cola, pk=task_id)
    return HttpResponse(get_log(task), mimetype='text/plain')

"""
Lista los vídeos que están pendientes de atención por parte del operador.
"""
@permission_required('postproduccion.video_manager')
def listar_pendientes(request):
    filtro = Q(status = 'PTO') | Q(status = 'ACE') | Q(status = 'REC')
    return render_to_response("postproduccion/pendientes.html", { 'list' : listar(filtro) }, context_instance=RequestContext(request))

"""
Lista los vídeos que están siendo procesados.
"""
@permission_required('postproduccion.video_manager')
def listar_en_proceso(request):
    return render_to_response("postproduccion/enproceso.html", { 'list' : listar() }, context_instance=RequestContext(request))

"""
Lista los vídeos que están siendo procesados que cumplan el filto dado.
"""
def listar(filtro = None):
    data = list()
    videolist = Video.objects.filter(~Q(status = 'LIS'))
    videolist = videolist.filter(filtro) if filtro else videolist
    for v in videolist.order_by('pk'):
        linea = dict()
        linea['id'] = v.pk
        linea['titulo'] = v.titulo
        linea['operador'] = v.informeproduccion.operador.username
        linea['fecha'] = v.informeproduccion.fecha_grabacion.strftime("%H:%M:%S - %d/%m/%Y")
        linea['tipo'] = v.status.lower()
        linea['status'] = dict(Video.VIDEO_STATUS)[v.status]
        data.append(linea)
    return data

"""
Vista para que el usuario verifique un vídeo y lo apruebe o rechace.
"""
def aprobacion_video(request, tk_str):
    v = token.is_valid_token(tk_str)
    if not v: raise Http404
    preview_url = reverse('postproduccion.views.stream_preview', args=(tk_str,))

    if request.method == 'POST':
        if request.POST['aprobado'] == 'true':
            v.informeproduccion.aprobado = True
            redirect = reverse('postproduccion.views.definir_metadatos_user', args=(tk_str,))
        else:
            v.informeproduccion.aprobado = False
            redirect = reverse('postproduccion.views.rechazar_video', args=(tk_str,))
        v.informeproduccion.save()
        return HttpResponseRedirect(redirect)

    return render_to_response("postproduccion/aprobacion_video.html", { 'v' : v, 'preview_url' : preview_url }, context_instance=RequestContext(request))

"""
Vista para que el usuario rellene los metadatos de un vídeo.
"""
def definir_metadatos_user(request, tk_str):
    v = token.is_valid_token(tk_str)
    if not v: raise Http404
    preview_url = reverse('postproduccion.views.stream_preview', args=(tk_str,))

    if request.method == 'POST':
        form = MetadataForm(request.POST, instance = v.metadata) if  hasattr(v, 'metadata') else MetadataForm(request.POST)
        if form.is_valid():
            m = form.save(commit = False)
            m.video = v
            m.save()
            token.token_attended(v)
            v.status = 'ACE'
            v.save()
            return HttpResponse("Datos enviados al operador para su aprobación")
    else:
        form = MetadataForm(instance = v.metadata) if hasattr(v, 'metadata') else MetadataForm()
    return render_to_response("postproduccion/definir_metadatos.html", { 'form' : form, 'v' : v, 'url' : preview_url }, context_instance=RequestContext(request))

"""
Vista para que el operador rellene los metadatos de un vídeo.
"""
@permission_required('postproduccion.video_manager')
def definir_metadatos_oper(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    video_url = reverse('postproduccion.views.stream_video', args = (video_id,))

    if request.method == 'POST':
        form = MetadataForm(request.POST)
        if form.is_valid():
            m = form.save(commit = False)
            m.video = v
            m.save()
            v.status = 'LIS'
            v.save()
            return HttpResponse("Puta madre, todo salvado")
    else:
        form = MetadataForm()
    return render_to_response("postproduccion/definir_metadatos.html", { 'form' : form, 'v' : v, 'url' : video_url }, context_instance=RequestContext(request))

"""
Solicita al usuario una razón por la cual el vídeo ha sido rechazado
"""
def rechazar_video(request, tk_str):
    v = token.is_valid_token(tk_str)
    if not v: raise Http404

    if request.method == 'POST':
        form = InformeRechazoForm(request.POST, instance = v.informeproduccion)
        if form.is_valid():
            form.save()
            token.token_attended(v)
            v.status = 'REC'
            v.save()
            return HttpResponse("Enviada notificación al operador para que atienda la incidencia")
    else:
        form = InformeRechazoForm()
    return render_to_response("postproduccion/rechazar_video.html", { 'form' : form, 'v' : v }, context_instance=RequestContext(request))

@permission_required('postproduccion.video_library')
def stream_video(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    resp = HttpResponse(utils.stream_file(v.fichero), mimetype='video/mp4')
    resp['Content-Length'] = os.path.getsize(v.fichero)
    return resp

def stream_preview(request, tk_str):
    v = token.is_valid_token(tk_str)
    resp = HttpResponse(utils.stream_file(v.previsualizacion.fichero), mimetype='video/x-flv')
    resp['Content-Length'] = os.path.getsize(v.previsualizacion.fichero)
    return resp

"""
Muestra el registro de eventos de la aplicación.
"""
@permission_required('postproduccion.video_manager')
def showlog(request, old = False):
    logdata = log.get_log() if not old else log.get_old_log()
    return render_to_response("postproduccion/log.html", { 'log' : logdata }, context_instance=RequestContext(request))

"""
Muestra las alertas de la aplicación.
"""
@permission_required('postproduccion.video_manager')
def alerts(request):
    lista = list()
    # Añade los vídeos incompletos.
    for i in Video.objects.filter(status='INC'):
        lista.append({ 'tipo' : 'video-incompleto', 'v' : i, 'fecha' : i.informeproduccion.fecha_grabacion })
    # Añade las tareas fallidas.
    for i in Cola.objects.filter(status='ERR'):
        lista.append({ 'tipo' : 'trabajo-fail', 't' : i, 'fecha' : i.comienzo })
    # Añade los tokens caducados.
    for i in token.get_expired_tokens():
        lista.append({ 'tipo' : 'token-caducado', 't' : i, 'fecha' : token.get_expire_time(i) })
    # Comprueba los ejecutables.
    if not utils.ffmpeg_version():
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'ffmpeg', 'fecha' : datetime.datetime.min })
    if not utils.melt_version():
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'melt', 'fecha' : datetime.datetime.min })
    if not utils.is_exec(config.get_option('CRONTAB_PATH')):
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'crontab', 'fecha' : datetime.datetime.min })
    # Comprueba las rutas a los directorios.
    for i in [config.get_option(x) for x in ['VIDEO_LIBRARY_PATH', 'VIDEO_INPUT_PATH', 'PREVIEWS_PATH']]:
        if not utils.check_dir(i):
            lista.append({ 'tipo' : 'ruta',  'path' : i, 'fecha' : datetime.datetime.min })
        else:
            cap = utils.df(i)[3]
            if int(cap.rstrip('%')) > 90:
                lista.append({ 'tipo' : 'disco', 'path' : i, 'cap' : cap, 'fecha' : datetime.datetime.min })
    # Ordena los elementos cronológicamente
    lista = sorted(lista, key=lambda it: it['fecha'])
    return render_to_response("postproduccion/alertas.html", { 'lista' : lista })

