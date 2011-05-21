# Create your views here.
# -*- encoding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from postproduccion.models import Video, Cola, FicheroEntrada
from postproduccion.forms import VideoForm, FicheroEntradaForm, RequiredBaseInlineFormSet, MetadataForm, InformeCreacionForm, ConfigForm, IncidenciaProduccionForm
from postproduccion import queue 
from postproduccion import utils
from postproduccion import token
from postproduccion import log
from postproduccion import crontab
from postproduccion import video
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
    utils.set_default_settings() # Fija la configuración por defecto si no existía configuración previa.
    return render_to_response("postproduccion/section-inicio.html", { }, context_instance=RequestContext(request))


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
            return redirect('postproduccion.views.fichero_entrada', v.id)
    else:
        vform = VideoForm(instance = v) if v else VideoForm()
        iform = InformeCreacionForm(instance = v.informeproduccion) if v else InformeCreacionForm()
    return render_to_response("postproduccion/section-nueva-paso1.html", { 'vform' : vform, 'iform' : iform }, context_instance=RequestContext(request))


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
            return redirect('postproduccion.views.resumen_video', v.id)
    else:
        if  v.ficheroentrada_set.count():
            fe = v.ficheroentrada_set.all()[0]
            fe.fichero = os.path.join('/', os.path.relpath(fe.fichero, config.get_option('VIDEO_INPUT_PATH')))
            form = FicheroEntradaForm(instance = fe)
        else:
            form = FicheroEntradaForm()
    return render_to_response("postproduccion/section-nueva-paso2-fichero.html", { 'v' : v, 'form' : form }, context_instance=RequestContext(request))

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
            return redirect('postproduccion.views.resumen_video', v.id)
    else:
        formset = FicheroEntradaFormSet(instance = v)
    
    for i in range(n):
        formset.forms[i].titulo = tipos[i].nombre
        if formset.forms[i].initial:
            formset.forms[i].initial['fichero'] = os.path.join('/', os.path.relpath(formset.forms[i].initial['fichero'], config.get_option('VIDEO_INPUT_PATH')))
    return render_to_response("postproduccion/section-nueva-paso2-ficheros.html", { 'v' : v, 'formset' : formset }, context_instance=RequestContext(request))

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
            queue.enqueue_pil(v)
        else:
            queue.enqueue_copy(v)
        v.set_status('DEF')
        messages.success(request, "Producción creada y encolada para su procesado")
        return redirect('postproduccion.views.estado_video', v.id)
    return render_to_response("postproduccion/section-nueva-paso3.html", { 'v' : v }, context_instance=RequestContext(request))

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

"""
Muestra la página del centro de monitorización.
"""
@permission_required('postproduccion.video_manager')
def centro_monitorizacion(request):
    return render_to_response("postproduccion/section-centro-monitorizacion.html", { }, context_instance=RequestContext(request))

@permission_required('postproduccion.video_manager')
def cola_base(request):
    return render_to_response("postproduccion/section-cola-base.html", context_instance=RequestContext(request))

@permission_required('postproduccion.video_manager')
def cola_listado(request):
    import json
    data = list()
    for task in Cola.objects.order_by('pk'):
        linea = dict()
        linea['v-titulo'] = task.video.titulo
        linea['v-url'] = reverse('estado_video', args=(task.video.id,))
        linea['tipo'] = dict(Cola.QUEUE_TYPE)[task.tipo]
        linea['comienzo'] = task.comienzo.strftime("%H:%M:%S - %d/%m/%Y") if task.comienzo else None
        linea['fin'] = task.fin.strftime("%H:%M:%S - %d/%m/%Y") if task.fin else None
        linea['logfile'] = task.logfile.name
        linea['logurl'] = reverse('postproduccion.views.mostrar_log', args=(task.pk,)) if task.logfile.name else None
        linea['id'] = task.pk
        linea['status'] = task.get_status_display()
        linea['progress'] = queue.progress(task) if task.status == 'PRO' else ''
        data.append(linea)
    return HttpResponse(json.dumps(data))

"""
Muestra el fichero de log para una tarea.
"""
@permission_required('postproduccion.video_manager')
def mostrar_log(request, task_id):
    task = get_object_or_404(Cola, pk=task_id)
    return HttpResponse(queue.get_log(task), mimetype='text/plain')

"""
Lista los vídeos que están pendientes de atención por parte del operador.
"""
@permission_required('postproduccion.video_manager')
def listar_pendientes(request):
    filtro = Q(status = 'PTO') | Q(status = 'ACE') | Q(status = 'REC')
    if request.is_ajax():
        return render_to_response("postproduccion/ajax/content-pendientes.html", { 'list' : listar(filtro)[:5] }, context_instance=RequestContext(request))
    else:
        return render_to_response("postproduccion/section-pendientes.html", { 'list' : listar(filtro) }, context_instance=RequestContext(request))

"""
Lista los vídeos que están siendo procesados.
"""
@permission_required('postproduccion.video_manager')
def listar_en_proceso(request):
    return render_to_response("postproduccion/section-enproceso.html", { 'list' : listar() }, context_instance=RequestContext(request))

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

    if v.informeproduccion.aprobado:
        return redirect('postproduccion.views.definir_metadatos_user', tk_str)

    if request.method == 'POST':
        form = IncidenciaProduccionForm(request.POST)
        if form.is_valid():
            inpro = form.save(commit = False)
            inpro.informe = v.informeproduccion
            inpro.emisor = 'U'
            if 'aprobado' in request.POST:
                inpro.aceptado = True
                v.informeproduccion.aprobado = True
                next_view = 'postproduccion.views.definir_metadatos_user'
            else:
                inpro.aceptado = False
                next_view = 'postproduccion.views.rechazar_video'
            v.informeproduccion.save()
            inpro.save()
        return redirect(next_view, tk_str)
    else:
        form = IncidenciaProduccionForm()

    return render_to_response("postproduccion/aprobacion_video.html", { 'v' : v, 'form' : form, 'token' : tk_str }, context_instance=RequestContext(request))

"""
Vista para que el usuario rellene los metadatos de un vídeo.
"""
def definir_metadatos_user(request, tk_str):
    v = token.is_valid_token(tk_str)
    if not v: raise Http404

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
    return render_to_response("postproduccion/definir_metadatos_user.html", { 'form' : form, 'v' : v, 'token' : tk_str }, context_instance=RequestContext(request))

"""
Solicita al usuario una razón por la cual el vídeo ha sido rechazado
"""
def rechazar_video(request, tk_str):
    v = token.is_valid_token(tk_str)
    if not v: raise Http404
    token.token_attended(v)
    v.status = 'REC'
    v.save()
    return render_to_response("postproduccion/rechazar_video.html", { 'v' : v })

#######
# Vistas para mostrar la información de una producción.
#######

"""
Vista para que el operador rellene los metadatos de un vídeo.
"""
@permission_required('postproduccion.video_manager')
def definir_metadatos_oper(request, video_id):
    v = get_object_or_404(Video, pk=video_id)

    if request.method == 'POST':
        form = MetadataForm(request.POST, instance = v.metadata) if  hasattr(v, 'metadata') else MetadataForm(request.POST)
        if form.is_valid():
            m = form.save(commit = False)
            m.video = v
            m.save()
            messages.success(request, 'Metadata actualizada')
    else:
        form = MetadataForm(instance = v.metadata) if hasattr(v, 'metadata') else MetadataForm()
    return render_to_response("postproduccion/definir_metadatos_oper.html", { 'form' : form, 'v' : v }, context_instance=RequestContext(request))


"""
Vista que muestra el estado e información de una producción.
"""
@permission_required('postproduccion.video_manager')
def estado_video(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    return render_to_response("postproduccion/estado_video.html", { 'v' : v }, context_instance=RequestContext(request))

"""
Muestra la información técnica del vídeo
"""
@permission_required('postproduccion.video_manager')
def media_info(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    info = video.parse_mediainfo(v.tecdata.txt_data) if hasattr(v, 'tecdata') else None
    return render_to_response("postproduccion/media_info.html", { 'v' : v, 'info' : info }, context_instance=RequestContext(request))

"""
Gestión de tickets de usuario.
"""
@permission_required('postproduccion.video_manager')
def gestion_tickets(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    tk = token.get_token_data(v)

    if request.method == 'POST':
        form = IncidenciaProduccionForm(request.POST)
        if form.is_valid():
            inpro = form.save(commit = False)
            inpro.informe = v.informeproduccion
            inpro.emisor = 'O'
            inpro.save()
            v.informeproduccion.aprobado = False
            v.informeproduccion.save()
            v.status = 'PTU'
            v.save()
            token.send_custom_mail_to_user(v, inpro.comentario)
            messages.success(request, "Ticket generado y enviado al usuario")
            return redirect('gestion_tickets', v.id)
    else:
        form = IncidenciaProduccionForm()

    return render_to_response("postproduccion/gestion_tickets.html", { 'v' : v, 'form' : form, 'token' : tk }, context_instance=RequestContext(request))

"""
Valida una producción y la pasa a la videoteca.
"""
@permission_required('postproduccion.video_manager')
def validar_produccion(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if hasattr(v, 'metadata'):
        v.status = 'LIS'
        v.save()
        queue.removeVideoTasks(v)
        messages.success(request, "Producción validada")
    else:
        messages.error(request, "Metadatos no definidos, no se puede validar")
    return redirect('estado_video', v.id)

"""
Borra una producción.
"""
@permission_required('postproduccion.video_manager')
def borrar_produccion(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    v.delete()
    messages.success(request, 'Producción eliminanada')
    return redirect('postproduccion.views.index')

#######

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
    return render_to_response("postproduccion/section-log.html", { 'log' : logdata, 'old' : old }, context_instance=RequestContext(request))

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
    if not utils.mediainfo_version():
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'mediainfo', 'fecha' : datetime.datetime.min })
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
    # Comprueba las tareas programadas
    if not crontab.status():
        lista.append({ 'tipo' : 'cron', 'fecha' : datetime.datetime.min })
    # Ordena los elementos cronológicamente
    lista = sorted(lista, key=lambda it: it['fecha'])
    if request.is_ajax():
        return render_to_response("postproduccion/ajax/content-alertas.html", { 'lista' : lista[:5] })
    else:
        return render_to_response("postproduccion/section-alertas.html", { 'lista' : lista })

"""
Edita los ajustes de configuración de la aplicación.
"""
@permission_required('postproduccion.video_manager')
def config_settings(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            for i in form.base_fields.keys():
                config.set_option(i.upper(), form.cleaned_data[i])
            messages.success(request, 'Configuración guardada')
    else:
        initial_data = dict()
        for i in ConfigForm.base_fields.keys():
            initial_data[i] = config.get_option(i.upper())
        form = ConfigForm(initial_data)
    return render_to_response("postproduccion/section-config.html", { 'form' : form }, context_instance=RequestContext(request))

"""
Muestra el estado de la aplicación con la configuración actual.
"""
@permission_required('postproduccion.video_manager')
def status(request):
    # Programas externos
    ffmpegver = utils.ffmpeg_version()
    meltver = utils.melt_version()
    mediainfover = utils.mediainfo_version()
    exes = {
        'FFMPEG'  : {
            'path'    : config.get_option('FFMPEG_PATH'),
            'status'  : True if ffmpegver else False,
            'version' : ffmpegver,
        },
        'MELT'    : {
            'path'    : config.get_option('MELT_PATH'),
            'status'  : True if meltver else False,
            'version' : meltver,
        },
        'crontab' : {
            'path'    : config.get_option('CRONTAB_PATH'),
            'status'  : utils.is_exec(config.get_option('CRONTAB_PATH')),
            'version' : 'N/A',
        },
        'mediainfo'    : {
            'path'    : config.get_option('MEDIAINFO_PATH'),
            'status'  : True if mediainfover else False,
            'version' : mediainfover,
        },
    }
    
    # Directorios
    dirs = dict()
    for i in [('library', 'VIDEO_LIBRARY_PATH'), ('input', 'VIDEO_INPUT_PATH'), ('previews', 'PREVIEWS_PATH')]:
        data = { 'path' : config.get_option(i[1]) }
        if utils.check_dir(data['path']):
            df = utils.df(data['path'])
            data['info'] = {
                'total' : df[0],
                'used'  : df[1],
                'left'  : df[2],
                'perc'  : df[3],
                'mount' : df[4]
            }
        dirs[i[0]] = data

    # Tareas Programadas
    if request.method == 'POST':
        if request.POST['status'] == '1':
            crontab.stop()
            messages.warning(request, 'Tareas programadas desactivadas')
        else:
            crontab.start()
            messages.success(request, 'Tareas programadas activadas')
    cron = crontab.status()

    return render_to_response("postproduccion/section-status.html", { 'exes' : exes, 'dirs' : dirs, 'cron' : cron }, context_instance=RequestContext(request))
