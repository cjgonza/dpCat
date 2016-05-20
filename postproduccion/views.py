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
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate, login

from postproduccion.models import Video, Cola, FicheroEntrada, IncidenciaProduccion, RegistroPublicacion, InformeProduccion
from postproduccion.forms import LoginForm, VideoForm, FicheroEntradaForm, RequiredBaseInlineFormSet, MetadataOAForm, MetadataGenForm, InformeCreacionForm, ConfigForm, ConfigMailForm, IncidenciaProduccionForm, VideoEditarForm, InformeEditarForm
from postproduccion import queue
from postproduccion import utils
from postproduccion import token
from postproduccion import log
from postproduccion import crontab
from postproduccion import video
from configuracion import config

from django.contrib.auth.models import User

import os
import urllib
import datetime

from django.contrib.auth.decorators import permission_required

'''
Login
'''
def login_view(request):
    if request.method == 'POST':
        lform = LoginForm(data=request.POST)
        if lform.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('postproduccion.views.index')
    else:
        lform = LoginForm()
    return render_to_response("postproduccion/login.html", { 'form' : lform }, context_instance=RequestContext(request))

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
        vform = VideoForm(request.POST, instance=v) if v else VideoForm(request.POST)
        iform = InformeCreacionForm(request.POST, instance=v.informeproduccion) if v else InformeCreacionForm(request.POST)
        if vform.is_valid():
            v = vform.save()
            i = iform.save(commit = False)
            i.video = v
            i.operador = request.user
            i.save()
            return redirect('postproduccion.views.fichero_entrada', v.id)
    else:
        vform = VideoForm(instance = v) if v else VideoForm()
        iform = InformeCreacionForm(instance = v.informeproduccion) if v else InformeCreacionForm(initial = { 'fecha_grabacion' : datetime.datetime.now() })
    return render_to_response("postproduccion/section-nueva-paso1.html", { 'vform' : vform, 'iform' : iform }, context_instance=RequestContext(request))


"""
Muestra el formulario para seleccionar el fichero de entrada.
"""
@permission_required('postproduccion.video_manager')
def _fichero_entrada_simple(request, v, type = None):
    if request.method == 'POST':
        form = FicheroEntradaForm(request.POST, instance = v.ficheroentrada_set.all()[0]) if v.ficheroentrada_set.count() else FicheroEntradaForm(request.POST)
        if form.is_valid():
            fe = form.save(commit = False)
            fe.video = v
            fe.fichero = os.path.normpath(config.get_option('VIDEO_INPUT_PATH') + fe.fichero)
            fe.save()
            if type == 'reemplazar_video':
                queue.enqueue_copy(v)
                v.set_status('DEF')
                messages.success(request, "Vídeo reemplazado y encolado para su procesado")
                return redirect('postproduccion.views.estado_video', v.id)
            else:
                return redirect('postproduccion.views.resumen_video', v.id)
    else:
        if  v.ficheroentrada_set.count():
            fe = v.ficheroentrada_set.all()[0]
            fe.fichero = os.path.join('/', os.path.relpath(fe.fichero, config.get_option('VIDEO_INPUT_PATH')))
            form = FicheroEntradaForm(instance = fe)
        else:
            form = FicheroEntradaForm()

    if type == 'reemplazar_video':
        return render_to_response("postproduccion/section-reemplazar-video.html", { 'v' : v, 'form' : form }, context_instance=RequestContext(request))
    else:
        return render_to_response("postproduccion/section-nueva-paso2-fichero.html", { 'v' : v, 'form' : form }, context_instance=RequestContext(request))

"""
Muestra el formulario para seleccionar los ficheros de entrada.
"""
@permission_required('postproduccion.video_manager')
def _fichero_entrada_multiple(request, v, type = None):
    n = v.plantilla.tipovideo_set.count()
    FicheroEntradaFormSet = inlineformset_factory(Video, FicheroEntrada, formset = RequiredBaseInlineFormSet, form = FicheroEntradaForm, extra = n, max_num = n, can_delete = False)
    tipos = v.plantilla.tipovideo_set.all().order_by('id')
    if request.method == 'POST':
        formset = FicheroEntradaFormSet(request.POST, instance = v) if v.ficheroentrada_set.count() else FicheroEntradaFormSet(request.POST)
        print "previo"
        if formset.is_valid():
            instances = formset.save(commit = False)
            for i in range(n):
                instances[i].fichero = os.path.normpath(config.get_option('VIDEO_INPUT_PATH') + instances[i].fichero)
                instances[i].video = v
                instances[i].tipo = tipos[i]
                instances[i].save()
            if type == 'reemplazar_video':
                queue.enqueue_pil(v)
                v.set_status('DEF')
                messages.success(request, "Vídeo reemplazado y encolado para su procesado")
                return redirect('postproduccion.views.estado_video', v.id)
            else:
                return redirect('postproduccion.views.resumen_video', v.id)
    else:
        formset = FicheroEntradaFormSet(instance = v)

    for i in range(n):
        formset.forms[i].titulo = tipos[i].nombre
        if formset.forms[i].initial:
            formset.forms[i].initial['fichero'] = os.path.join('/', os.path.relpath(formset.forms[i].initial['fichero'], config.get_option('VIDEO_INPUT_PATH')))

    if type == 'reemplazar_video':
        return render_to_response("postproduccion/section-reemplazar-videos.html", { 'v' : v, 'formset' : formset }, context_instance=RequestContext(request))
    else:
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
        return redirect('index')
    return render_to_response("postproduccion/section-nueva-paso3.html", { 'v' : v }, context_instance=RequestContext(request))

"""
Devuelve una lista (html) con el contenido de un directorio para usar con la
llamada AJAX del jqueryFileTree.
"""
@permission_required('postproduccion.video_manager')
@csrf_exempt
def dirlist(request):
    r = ['<ul class="jqueryFileTree" style="display: none;">']
    try:
        basedir = urllib.unquote(config.get_option('VIDEO_INPUT_PATH')).encode('utf-8')
        reqdir = urllib.unquote(request.POST.get('dir')).encode('utf-8')
        fulldir = os.path.normpath(basedir + reqdir)
        for f in sorted(os.listdir(fulldir)):
            if f.startswith('.'): continue
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
    return HttpResponse(queue.get_log(task), content_type='text/plain')

"""
Lista los vídeos que están pendientes de atención por parte del operador.
"""
@permission_required('postproduccion.video_manager')
def listar_pendientes(request):
    filtro = Q(status = 'PTO') | Q(status = 'ACE') | Q(status = 'REC')
    if request.is_ajax():
        return render_to_response("postproduccion/ajax/content-pendientes.html", { 'list' : listar(filtro=filtro)[:5] }, context_instance=RequestContext(request))
    else:
        return render_to_response("postproduccion/section-pendientes.html", { 'list' : listar(filtro=filtro) }, context_instance=RequestContext(request))

"""
Lista los vídeos que están siendo procesados.
"""
@permission_required('postproduccion.video_manager')
def listar_en_proceso(request):
    operator_id = request.GET.get('operator_id')
    archivados = request.GET.get('archivados')

    op_id = get_object_or_404(User, id=operator_id) if operator_id else None

    if request.is_ajax():
        return render_to_response("postproduccion/ajax/content-enproceso.html", { 'list' : listar(archivados, operator_id=op_id)[:10] }, context_instance=RequestContext(request))
    else:
        return render_to_response("postproduccion/section-enproceso.html", { 'list' : listar(archivados, operator_id=op_id) , 'usuarios' : User.objects.all()}, context_instance=RequestContext(request))

"""
Lista los vídeos que están siendo procesados que cumplan el filto dado.
"""
def listar(archivados = None, operator_id = None, filtro = None):
    data = list()
    if operator_id:#si se esta filtrando por operador hay que coger los videos desde imforme de produccion
        informes_produccion = InformeProduccion.objects.filter(operador = operator_id).exclude(video__status = 'LIS').filter(id__gt = 2179)
        if archivados == None:
            informes_produccion = informes_produccion.exclude(video__archivado = True)
        for v in informes_produccion.order_by('pk'):
            data.append(get_linea(v.video))
    else:#si no listamos todos los videos
        videolist = Video.objects.exclude(status = 'LIS').filter(id__gt = 2179)
        if archivados == None:
            videolist = videolist.exclude(archivado = True)
        videolist = videolist.filter(filtro) if filtro else videolist
        for v in videolist.order_by('pk'):
            data.append(get_linea(v))
    return data

'''
Contruye una entrada con los datos de un video que toma como argumento
'''
def get_linea(video):
    linea = dict()
    linea['id'] = video.pk
    linea['titulo'] = video.titulo
    linea['operador'] = video.informeproduccion.operador.username
    linea['fecha'] = video.informeproduccion.fecha_produccion.strftime("%d/%m/%Y")
    linea['responsable'] = video.autor
    linea['tipo'] = video.status.lower()
    linea['status'] = dict(Video.VIDEO_STATUS)[video.status]
    linea['archivado'] = video.archivado
    return linea

"""
Lista las últimas producciones incluidas en la videoteca.
"""
@permission_required('postproduccion.video_manager')
def ultimas_producciones(request):
    videolist = Video.objects.filter(status = 'LIS').order_by('-informeproduccion__fecha_validacion')
    return render_to_response("postproduccion/ajax/content-ultimas.html", { 'videos' : videolist[:5] }, context_instance=RequestContext(request))

#######
# Vistas públicas para que el usuario acepte una producción.
#######

"""
Vista para que el usuario verifique un vídeo y lo apruebe o rechace.
"""
def aprobacion_video(request, tk_str):
    v = token.is_valid_token(tk_str)
    if not v: return render_to_response("postproduccion/section-ticket-caducado.html")
    return render_to_response("postproduccion/section-inicio-aprobacion.html", { 'v' : v, 'token' : tk_str }, context_instance=RequestContext(request))

"""
Vista para que el usuario rellene los metadatos de un vídeo.
"""
def definir_metadatos_user(request, tk_str):
    v = token.is_valid_token(tk_str)
    if not v: return render_to_response("postproduccion/section-ticket-caducado.html")

    if v.objecto_aprendizaje:
        MetadataForm = MetadataOAForm
        metadataField = 'metadataoa'
    else:
        MetadataForm = MetadataGenForm
        metadataField = 'metadatagen'

    initial_data = {
        'title' : v.titulo,
        'creator' : v.autor
    }

    if request.method == 'POST':

        form = MetadataForm(request.POST, instance = getattr(v, metadataField)) if  hasattr(v, metadataField) else MetadataForm(request.POST, initial = initial_data)
        if form.is_valid():
            m = form.save(commit = False)
            m.video = v
            m.date = v.informeproduccion.fecha_grabacion
            m.created = v.informeproduccion.fecha_produccion
            m.save()
            inpro = IncidenciaProduccion(informe = v.informeproduccion, aceptado = True)
            inpro.save()
            token.token_attended(v)
            v.status = 'ACE'
            v.save()
            video.add_metadata(v)
            return render_to_response("postproduccion/section-resumen-aprobacion.html", { 'v' : v, 'aprobado' : True }, context_instance=RequestContext(request))

    else:
        form = MetadataForm(instance = getattr(v, metadataField)) if hasattr(v, metadataField) else MetadataForm(initial = initial_data)

    return render_to_response("postproduccion/section-metadatos-user.html", { 'form' : form, 'v' : v, 'token' : tk_str }, context_instance=RequestContext(request))

"""
Solicita al usuario una razón por la cual el vídeo ha sido rechazado
"""
def rechazar_video(request, tk_str):
    v = token.is_valid_token(tk_str)
    if not v: return render_to_response("postproduccion/section-ticket-caducado.html")

    if request.method == 'POST':
        form = IncidenciaProduccionForm(request.POST)
        if form.is_valid():
            inpro = form.save(commit = False)
            inpro.informe = v.informeproduccion
            inpro.aceptado = False
            inpro.save()
            token.token_attended(v)
            v.status = 'REC'
            v.save()
            return render_to_response("postproduccion/section-resumen-aprobacion.html", { 'v' : v, 'aprobado' : False }, context_instance=RequestContext(request))
    else:
        form = IncidenciaProduccionForm()
    return render_to_response("postproduccion/section-rechazar-produccion.html", { 'v' : v, 'form' : form, 'token' : tk_str }, context_instance=RequestContext(request))

#######
# Vistas para reemplazar un video de una producción existente
#######
@permission_required('postproduccion.video_manager')
def reemplazar_video(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if v.plantilla:
        return _fichero_entrada_multiple(request, v, type = 'reemplazar_video')
    else:
        return _fichero_entrada_simple(request, v, type = 'reemplazar_video')

#######
# Vistas para mostrar la información de una producción.
#######

"""
Vista para que el operador rellene los metadatos de un vídeo.
"""
@permission_required('postproduccion.video_manager')
def definir_metadatos_oper(request, video_id):

    v = get_object_or_404(Video, pk=video_id)

    if v.objecto_aprendizaje:
        MetadataForm = MetadataOAForm
        metadataField = 'metadataoa'
    else:
        MetadataForm = MetadataGenForm
        metadataField = 'metadatagen'

    initial_data = {
        'title' : v.titulo,
        'creator' : v.autor
    }

    if request.method == 'POST':
        form = MetadataForm(request.POST, instance = getattr(v, metadataField)) if  hasattr(v, metadataField) else MetadataForm(request.POST, initial = initial_data)
        if form.is_valid():
            m = form.save(commit = False)
            m.video = v
            m.date = v.informeproduccion.fecha_grabacion
            m.created = v.informeproduccion.fecha_produccion
            m.save()
            video.add_metadata(v)
            messages.success(request, 'Metadata actualizada')
    else:
        form = MetadataForm(instance = getattr(v, metadataField)) if hasattr(v, metadataField) else MetadataForm(initial = initial_data)

    return render_to_response("postproduccion/section-metadatos-oper.html", { 'form' : form, 'v' : v }, context_instance=RequestContext(request))


"""
Vista que muestra el estado e información de una producción.
"""
@permission_required('postproduccion.video_manager')
def estado_video(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    pub = RegistroPublicacion.objects.filter(video__id=v.id)
    return render_to_response("postproduccion/section-resumen-produccion.html", { 'v' : v, 'pub' : pub }, context_instance=RequestContext(request))

"""
Muestra la información técnica del vídeo
"""
@permission_required('postproduccion.video_manager')
def media_info(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    info = video.parse_mediainfo(v.tecdata.txt_data) if hasattr(v, 'tecdata') else None
    return render_to_response("postproduccion/section-metadata-tecnica.html", { 'v' : v, 'info' : info }, context_instance=RequestContext(request))

"""
Devuelve la información técnica del vídeo en XML para su descarga.
"""
@permission_required('postproduccion.video_manager')
def download_media_info(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    response = HttpResponse(v.tecdata.xml_data, content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=%d.xml' % v.id
    return response

"""
Gestión de tickets de usuario.
"""
@permission_required('postproduccion.video_manager')
def gestion_tickets(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if v.status == 'LIS': raise Http404
    tk = token.get_token_data(v)

    if request.method == 'POST':
        form = IncidenciaProduccionForm(request.POST)
        if form.is_valid():
            inpro = form.save(commit = False)
            inpro.informe = v.informeproduccion
            inpro.emisor = request.user
            inpro.save()
            v.status = 'PTU'
            v.save()
            if token.send_custom_mail_to_user(v, inpro.comentario, request.user.first_name) is None:
                messages.success(request, "Ticket generado")
                messages.error(request, "No se ha podido enviar al usuario")
            else:
                messages.success(request, "Ticket generado y enviado al usuario")
            return redirect('gestion_tickets', v.id)
    else:
        form = IncidenciaProduccionForm()

    return render_to_response("postproduccion/section-gestion-tickets.html", { 'v' : v, 'form' : form, 'token' : tk }, context_instance=RequestContext(request))

"""
Regenerar tickets mediante checkbox
"""
@permission_required('postproduccion.video_manager')
def regenerar_tickets(request):
    if request.method == 'POST':
        videos = Video.objects.filter(pk__in=request.POST.getlist('ticket'))
        for v in videos:
            if v.status == 'LIS': continue
            v.status = 'PTU'
            v.save()
            if token.send_custom_mail_to_user(v, ('regenerar ticket %s' % v.titulo), request.user.first_name) is None:
                messages.error(request, "No se ha podido enviar al usuario")
        messages.success(request, "Tickets regenerados")

    return redirect('enproceso')
"""
Archivar/desarchivar videos mediante checkbox
"""
@permission_required('postproduccion.video_manager')
def archivar_desarchivar(request):
    if request.method == 'POST':
        videos = Video.objects.filter(pk__in=request.POST.getlist('ticket'))
        for v in videos:
            if v.archivado == True:
                v.archivado = False
                v.save()
            else:
                v.archivado = True
                v.save()

        messages.success(request, "Prceso de archivado realizado correctamente")

    return redirect('enproceso')

"""
Edita la información básica de la producción.
"""
@permission_required('postproduccion.video_manager')
def editar_produccion(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    if v.status == 'LIS': raise Http404

    if request.method == 'POST':
        vform = VideoEditarForm(request.POST, instance=v)
        iform = InformeEditarForm(request.POST, instance=v.informeproduccion)
        if vform.is_valid():
            v = vform.save()
            i = iform.save()
            if v.objecto_aprendizaje and hasattr(v, 'metadatagen'):
                v.metadatagen.delete()
                messages.error(request, u'Eliminada la metadata previamente asociada a la producción')
            if not v.objecto_aprendizaje and hasattr(v, 'metadataoa'):
                v.metadataoa.delete()
                messages.error(request, u'Eliminada la metadata previamente asociada a la producción')
            messages.success(request, u'Actualizada la información básica de la producción')
    else:
        vform = VideoEditarForm(instance = v)
        iform = InformeEditarForm(instance = v.informeproduccion)
    return  render_to_response("postproduccion/section-editar-info.html", { 'v' : v, 'vform' : vform, 'iform' : iform }, context_instance=RequestContext(request))

"""
Valida una producción y la pasa a la videoteca.
"""
@permission_required('postproduccion.video_manager')
def validar_produccion(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    metadataField = 'metadataoa' if v.objecto_aprendizaje else 'metadatagen'
    if hasattr(v, metadataField):
        v.informeproduccion.fecha_validacion = datetime.datetime.now()
        v.informeproduccion.save()
        getattr(v, metadataField).valid = v.informeproduccion.fecha_validacion
        getattr(v, metadataField).save()
        v.status = 'LIS'
        v.save()
        #if v.informeproduccion.aprobacion:
        #    token.send_validation_mail_to_user(v, request.user.first_name)
        queue.removeVideoTasks(v)
        if v.informeproduccion.aprobacion:
            v.previsualizacion.delete()
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
    messages.success(request, 'Producción eliminada con éxito.')
    return redirect('postproduccion.views.index')

"""
Envía un correo al autor notificando de que una producción se encuentra publicada.
"""
@permission_required('postproduccion.video_manager')
def notificar_publicacion(request, record_id):
    r = get_object_or_404(RegistroPublicacion, pk = record_id)
    if token.send_published_mail_to_user(r) is None:
        messages.error(request, u'No se ha podido enviar la notificación al autor')
    else:
        messages.success(request, u'Enviado correo de notificación de publicacion al autor')
    return redirect('estado_video', r.video.id)

"""
Borra el registro de publicación dado.
"""
@permission_required('postproduccion.video_manager')
def borrar_registro(request, record_id):
    r = get_object_or_404(RegistroPublicacion, pk = record_id)
    v = r.video
    r.delete()
    messages.success(request, u'Registro de publicación eliminado')
    return redirect('estado_video', v.id)

"""
Muestra la videoteca.
"""
@permission_required('postproduccion.video_manager')
def videoteca(request):
    video_list = Video.objects.filter(status = 'LIS').order_by('-informeproduccion__fecha_validacion')
    publicados = RegistroPublicacion.objects.all().values_list('video', flat= True)

    autor = request.GET.get('autor')
    titulo = request.GET.get('titulo')
    vid = request.GET.get('id')
    tipoVideoSearch = request.GET.get('tipoVideo')
    meta_titulo = request.GET.get('meta_titulo')
    meta_autor = request.GET.get('meta_autor')
    meta_descripcion = request.GET.get('meta_descripcion')
    meta_etiqueta = request.GET.get('meta_etiqueta')
    try:
        f_ini = datetime.datetime.strptime(request.GET.get('f_ini'), "%d/%m/%Y")
    except (ValueError, TypeError):
        f_ini = None
    try:
        f_fin = datetime.datetime.strptime(request.GET.get('f_fin'), "%d/%m/%Y")
    except (ValueError, TypeError):
        f_fin = None

    if autor:
        video_list = video_list.filter(autor__icontains = autor)
    if titulo:
        video_list = video_list.filter(titulo__icontains = titulo)
    if vid:
        video_list = video_list.filter(pk = vid)
    if meta_titulo:
        video_list = video_list.filter(Q(metadatagen__title__icontains=meta_titulo) | Q(metadataoa__title__icontains=meta_titulo))
    if meta_autor:
        video_list = video_list.filter(Q(metadatagen__creator__icontains=meta_autor) | Q(metadataoa__creator__icontains=meta_autor))
    if meta_descripcion:
        video_list = video_list.filter(Q(metadatagen__description__icontains=meta_descripcion) | Q(metadataoa__description__icontains=meta_descripcion))
    if meta_etiqueta:
        video_list = video_list.filter(Q(metadatagen__keyword__icontains=meta_etiqueta) | Q(metadataoa__keyword__icontains=meta_etiqueta))
    if tipoVideoSearch and tipoVideoSearch != 'UNK':
        video_list = video_list.filter(tipoVideo = tipoVideoSearch)

    video_list = video_list.filter(informeproduccion__fecha_validacion__range = (f_ini or datetime.date.min, f_fin or datetime.date.max))


    try:
        nresults = int(request.GET.get('nresults', 25))
    except ValueError:
        nresults = 25

    paginator = Paginator(video_list, nresults)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        videos = paginator.page(page)
    except (EmptyPage, InvalidPage):
        videos = paginator.page(paginator.num_pages)

    return render_to_response("postproduccion/section-videoteca.html", { 'videos' : videos, 'pub' : publicados, 'tipoVideo' : Video.VIDEO_TYPE }, context_instance=RequestContext(request))

"""
Mostrar estadísticas de la videoteca
"""
@permission_required('postproduccion.video_manager')
def estadisticas(request):
    videos = Video.objects.all()

    # Personalizacion de resultados por fecha
    try:
        f_ini = datetime.datetime.strptime(request.GET.get('f_ini'), "%d/%m/%Y")
    except (ValueError, TypeError):
        f_ini = None
    try:
        f_fin = datetime.datetime.strptime(request.GET.get('f_fin'), "%d/%m/%Y")
    except (ValueError, TypeError):
        f_fin = None

    videos = videos.filter(informeproduccion__fecha_grabacion__range = (f_ini or datetime.date.min, f_fin or datetime.date.max))

    # Estadisticas
    n_prod = [
        ['Producciones realizadas', videos.count(), video.get_duration(videos)],
        ['Producciones validadas', videos.filter(status='LIS').count(), video.get_duration(videos.filter(status='LIS'))],
        ['Pildoras', videos.exclude(plantilla=None).count(), video.get_duration(videos.exclude(plantilla=None))],
        ['Producciones propias', videos.filter(plantilla=None).count(), video.get_duration(videos.filter(plantilla=None))]
    ]

    return render_to_response("postproduccion/section-estadisticas.html", { 'stats': n_prod }, context_instance=RequestContext(request))

#######

@permission_required('postproduccion.video_library')
def stream_video(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    resp = HttpResponse(utils.stream_file(v.fichero), content_type='video/mp4')
    resp['Content-Length'] = os.path.getsize(v.fichero)
    return resp

@permission_required('postproduccion.video_library')
def download_video(request, video_id):
    v = get_object_or_404(Video, pk=video_id)
    resp = HttpResponse(utils.stream_file(v.fichero), content_type='video/mp4')
    resp['Content-Length'] = os.path.getsize(v.fichero)
    resp['Content-Disposition'] = "attachment;filename=%d_%s.mp4" % (v.id, utils.normalize_filename(v.titulo))
    return resp

def stream_preview(request, tk_str):
    v = token.is_valid_token(tk_str)
    resp = HttpResponse(utils.stream_file(v.previsualizacion.fichero), content_type='video/mp4')
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
    tipo = {
        'video-incompleto' : 'Video incompleto',
        'trabajo-fail' : 'Tarea fallida',
        'token-caducado' : 'Token caducado',
        'video-aceptado' : 'Video sin validar',
        'ejecutable' : 'Ejecutable',
        'ruta' : 'Ruta',
        'disco' : 'Disco',
        'cron_proc' : 'Tarea programada'
    }

    tipoVideo = request.GET.get('tipoVideo')

    # Añade los vídeos incompletos.
    for i in Video.objects.filter(status='INC'):
        lista.append({ 'tipo' : 'video-incompleto', 'v' : i, 'fecha' : i.informeproduccion.fecha_produccion })
    # Añade las tareas fallidas.
    for i in Cola.objects.filter(status='ERR'):
        lista.append({ 'tipo' : 'trabajo-fail', 't' : i, 'fecha' : i.comienzo })
    # Añade los tokens caducados.
    for i in token.get_expired_tokens():
        lista.append({ 'tipo' : 'token-caducado', 't' : i, 'fecha' : token.get_expire_time(i) })
    # Añade los vídeos aceptados pendientes de validación.
    for i in InformeProduccion.objects.filter(
            video=Video.objects.filter(status='ACE'),
            fecha_produccion__lt = datetime.datetime.today() - datetime.timedelta(days = 15)):
        lista.append({ 'tipo' : 'video-aceptado', 'v' : i.video , 'fecha' : i.fecha_produccion })
    # Comprueba los ejecutables.
    if not utils.avconv_version():
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'avconv', 'fecha' : datetime.datetime.min })
    if not utils.melt_version():
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'melt', 'fecha' : datetime.datetime.min })
    if not utils.mediainfo_version():
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'mediainfo', 'fecha' : datetime.datetime.min })
    if not utils.mp4box_version():
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'MP4Box', 'fecha' : datetime.datetime.min })
    if not utils.exiftool_version():
        lista.append({ 'tipo' : 'ejecutable', 'exe' : 'exiftool', 'fecha' : datetime.datetime.min })
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
    if not crontab.status('procesar_video'):
        lista.append({ 'tipo' : 'cron_proc', 'fecha' : datetime.datetime.min })
    if not crontab.status('publicar_video'):
        lista.append({ 'tipo' : 'cron_pub', 'fecha' : datetime.datetime.min })

    # Filtrar por tipo de video
    if tipoVideo is not None:
        lista = [element for element in lista if element['tipo'] == tipoVideo]
    # Ordena los elementos cronológicamente
    lista = sorted(lista, key=lambda it: it['fecha'])

    if request.is_ajax():
        return render_to_response("postproduccion/ajax/content-alertas.html", { 'lista' : lista[:5] }, context_instance=RequestContext(request))
    else:
        return render_to_response("postproduccion/section-alertas.html", { 'lista' : lista , 'tipoAlerta' : tipo}, context_instance=RequestContext(request))

"""
Edita los ajustes de configuración de la aplicación.
"""
@permission_required('postproduccion.video_manager')
def config_settings(request, mail = False):
    ClassForm = ConfigMailForm if mail else ConfigForm
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            for i in form.base_fields.keys():
                config.set_option(i.upper(), form.cleaned_data[i])
            messages.success(request, 'Configuración guardada')
    else:
        initial_data = dict()
        for i in ClassForm.base_fields.keys():
            initial_data[i] = config.get_option(i.upper())
        form = ClassForm(initial_data)
    return render_to_response("postproduccion/section-config.html", { 'form' : form, 'mail' : mail }, context_instance=RequestContext(request))

"""
Muestra el estado de la aplicación con la configuración actual.
"""
@permission_required('postproduccion.video_manager')
def status(request):
    # Programas externos
    avconvver = utils.avconv_version()
    meltver = utils.melt_version()
    mediainfover = utils.mediainfo_version()
    mp4boxver = utils.mp4box_version()
    exiftoolver = utils.exiftool_version()
    exes = {
        'AVCONV'  : {
            'path'    : config.get_option('AVCONV_PATH'),
            'status'  : True if avconvver else False,
            'version' : avconvver,
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
        'MP4Box'    : {
            'path'    : config.get_option('MP4BOX_PATH'),
            'status'  : True if mp4boxver else False,
            'version' : mp4boxver,
        },
        'exiftool'    : {
            'path'    : config.get_option('EXIFTOOL_PATH'),
            'status'  : True if exiftoolver else False,
            'version' : exiftoolver,
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
        if 'status_process' in request.POST:
            if request.POST['status_process'] == '1':
                crontab.stop('procesar_video')
                messages.warning(request, 'Tareas programadas de codificación desactivadas')
            else:
                crontab.start('procesar_video')
                messages.success(request, 'Tareas programadas de codificacion activadas')
        if 'status_publish' in request.POST:
            if request.POST['status_publish'] == '1':
                crontab.stop('publicar_video')
                messages.warning(request, 'Tareas programadas de publicación desactivadas')
            else:
                crontab.start('publicar_video')
                messages.success(request, 'Tareas programadas de publicación activadas')
    cron = { 'process' : crontab.status('procesar_video'), 'publish' : crontab.status('publicar_video') }

    # Información de la versión
    dpcatinfo = utils.dpcat_info()
    version = [
        ['Versión', dpcatinfo['version']],
        ['Rama', dpcatinfo['branch']],
        ['Commit', dpcatinfo['commit']],
        ['Repositorio', dpcatinfo['url']],
        ['Fecha', dpcatinfo['date']],
        ['Autor', dpcatinfo['author']],
        ['Mensaje', dpcatinfo['message']]
    ]

    return render_to_response("postproduccion/section-status.html", { 'exes' : exes, 'dirs' : dirs, 'cron' : cron, 'version' : version }, context_instance=RequestContext(request))
