#encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from postproduccion import utils

import os
import signal

# Create your models here.

class PlantillaFDV(models.Model):   # (Fondo-Disapositiva-Video)
    nombre = models.CharField(max_length = 50)

    fondo = models.ImageField(upload_to = 'plantillas')

    class Meta:
        verbose_name = u'Plantilla Fondo-Diapositiva-Vídeo'

    def __unicode__(self):
        return self.nombre

class TipoVideo(models.Model):
    nombre = models.CharField(max_length = 30)
    plantilla =  models.ForeignKey(PlantillaFDV)

    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    ancho = models.PositiveSmallIntegerField()
    alto = models.PositiveSmallIntegerField()
    mix = models.PositiveSmallIntegerField(default = 100)

    def __unicode__(self):
        return self.nombre

class Video(models.Model):
    VIDEO_STATUS = (
        ('INC', u'Incompleto'),                  # Creado pero sin ficheros de entrada.
        ('DEF', u'Definido'),                    # Definidos los ficheros de entrada (en cola para ser procesado).
        ('PRV', u'Procesando vídeo'),            # Está siendo procesado (montaje o copia).
        ('COM', u'Completado'),                  # Procesamiento completado (en cola para generar previsualización).
        ('PRP', u'Procesando previsualización'), # Está siendo generada la previsualización.
        ('PTU', u'Pendiente del usuario'),       # A la espera de que el usuario rellene los metadatos y acepte el vídeo.
        ('PTO', u'Pendiente del operador'),      # A la espera de que el operador rellene los metadatos.
        ('ACE', u'Aceptado'),                    # Aceptado por el usuario, a la espera de que lo valide el operador.
        ('REC', u'Rechazado'),                   # Rechazado por el usuario, a la espera de que el operador tome las medidas necesarias.
        ('LIS', u'Listo'),                       # Validado por el operador, todos los procedimientos terminados.
    )

    fichero = models.CharField(max_length = 255, editable = False)
    status = models.CharField(max_length = 3, choices = VIDEO_STATUS, editable = False, default = 'INC')
    plantilla = models.ForeignKey(PlantillaFDV, null = True, blank = True)

 
    titulo = models.CharField(max_length = 30)
    autor = models.CharField(max_length = 30)
    email = models.EmailField()

    def __unicode__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        for task in self.cola_set.all():
            task.delete()
        if self.fichero:
            utils.remove_file_path(self.fichero)
        if hasattr(self, 'previsualizacion'):
            self.previsualizacion.delete()
        super(Video, self).delete(*args, **kwargs)

    def set_status(self, st):
        self.status = st
        self.save()

    class Meta:
        permissions = (
            ("video_manager", u"Puede gestionar la creación de vídeos"),
            ("video_library", u"Puede consultar la videoteca"),
        )

class InformeProduccion(models.Model):
    video = models.OneToOneField(Video, editable = False)
    operador = models.ForeignKey(User, editable = False)
    observacion = models.TextField(null = True, blank = True)
    fecha_grabacion = models.DateTimeField(auto_now_add = True)
    aprobacion = models.BooleanField(default = True)
    aprobado = models.BooleanField(default = False)

class IncidenciaProduccion(models.Model):
    WHO = (
        ('O', u'Operador'),
        ('U', u'Usuario'),
    )

    
    informe = models.ForeignKey(InformeProduccion, editable = False)
    emisor = models.CharField(max_length = 1, choices = WHO, editable = False)
    comentario = models.TextField()
    fecha =  models.DateTimeField(auto_now_add = True)
    aceptado = models.NullBooleanField()

class HistoricoCodificacion(models.Model):
    TASK_TYPE = (
        ('COP', u'Copia'),
        ('PIL', u'Píldora'),
        ('PRE', u'Previsualización')
    )

    informe = models.ForeignKey(InformeProduccion, editable = False)
    tipo = models.CharField(max_length = 3, choices = TASK_TYPE)
    fecha = models.DateTimeField()
    status = models.BooleanField()

class FicheroEntrada(models.Model):
    video = models.ForeignKey(Video, editable = False)
    tipo = models.ForeignKey(TipoVideo, editable = False, null = True)
    fichero = models.CharField(max_length = 255)

    def __unicode__(self):
        if self.tipo:
            return "%s (%s)" % (self.video.titulo, self.tipo.nombre)
        return self.video.titulo

class TecData(models.Model):
    xml_data = models.TextField(null = True)
    txt_data = models.TextField(null = True)

    video = models.OneToOneField(Video)

    class Meta:
        verbose_name = u'Información técnica'
        verbose_name_plural = u'Informaciones técnicas'

    def __unicode__(self):
        return self.video.titulo

class Previsualizacion(models.Model):
    video = models.OneToOneField(Video)
    fichero = models.CharField(max_length = 255)

    def delete(self, *args, **kwargs):
        if self.fichero:
            utils.remove_file_path(self.fichero)
        super(Previsualizacion, self).delete(*args, **kwargs)

class Metadata(models.Model):
    video = models.OneToOneField(Video, editable = False)

    # TODO: Metadatos iniciales a modo de ejemplo, cambiar por los definitivos.
    titulo = models.CharField(max_length = 30)
    subtitulo = models.CharField(max_length = 100)
    descripcion = models.TextField()
    autor = models.CharField(max_length = 30)

    class Meta:
        verbose_name = u'Metadatos'
        verbose_name_plural = u'Metadatos'

    def __unicode__(self):
        return self.video.titulo


## COLA ##

class ColaManager(models.Manager):
    """
    Devuelve el número de trabajos que están siendo codificados en este momento.
    """
    def count_actives(self):
        return super(ColaManager, self).get_query_set().filter(status = 'PRO').count()

    """
    Devuelve el número de trabajos que están pendientes de ser procesados
    """
    def count_pendings(self):
        return super(ColaManager, self).get_query_set().filter(status = 'PEN').count()

    """
    Devuelve la lista de vídeos pendientes de ser procesados.
    """
    def get_pendings(self):
         return super(ColaManager, self).get_query_set().filter(status = 'PEN').order_by('id')

class Cola(models.Model):
    QUEUE_STATUS = (
        ('PEN', 'Pendiente'),
        ('PRO', 'Procesando'),
        ('HEC', 'Hecho'),
        ('ERR', 'Error'),
    )

    QUEUE_TYPE = (
        ('COP', u'Copia'),
        ('PIL', u'Producción'),
        ('PRE', u'Previsualización')
    )

    objects = ColaManager()

    video = models.ForeignKey(Video)
    status = models.CharField(max_length = 3, choices = QUEUE_STATUS, default = 'PEN')
    tipo = models.CharField(max_length = 3, choices = QUEUE_TYPE)
    comienzo = models.DateTimeField(null = True, blank = True)
    fin = models.DateTimeField(null = True, blank = True)
    logfile = models.FileField(upload_to = "logs", null = True, blank = True)
    pid = models.IntegerField(null = True, editable = False)

    def __unicode__(self):
       return dict(self.QUEUE_TYPE)[self.tipo] + ": " + self.video.__unicode__()

    def set_status(self, st):
        self.status = st
        self.save()

    def delete(self, *args, **kwargs):
        if self.status == 'PRO' and self.pid:
            os.kill(self.pid, signal.SIGTERM)
            while Cola.objects.get(pk=self.id).status == 'PRO': pass
        super(Cola, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = u'tarea'
        verbose_name_plural = u'tareas'

class Token(models.Model):

    token = models.CharField(max_length = 25)
    instante = models.DateTimeField(auto_now_add = True)
    video = models.OneToOneField(Video)

    def __unicode__(self):
        return self.video.titulo
