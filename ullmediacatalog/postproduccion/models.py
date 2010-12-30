#encoding: utf-8
from django.db import models
from postproduccion import utils

# Create your models here.

class TipoVideo(models.Model):
    nombre = models.CharField(max_length = 30)

    def __unicode__(self):
        return self.nombre

class PlantillaFDV(models.Model):   # (Fondo-Disapositiva-Video)
    nombre = models.CharField(max_length = 50)

    fondo = models.ImageField(upload_to = 'plantillas')

    diapositiva_tipo = models.ForeignKey(TipoVideo, related_name = "t_diap")
    diapositiva_x = models.PositiveSmallIntegerField()
    diapositiva_y = models.PositiveSmallIntegerField()
    diapositiva_ancho = models.PositiveSmallIntegerField()
    diapositiva_alto = models.PositiveSmallIntegerField()
    diapositiva_mix = models.PositiveSmallIntegerField(default = 100)

    video_tipo = models.ForeignKey(TipoVideo, related_name = "t_vid")
    video_x = models.PositiveSmallIntegerField()
    video_y = models.PositiveSmallIntegerField()
    video_ancho = models.PositiveSmallIntegerField()
    video_alto = models.PositiveSmallIntegerField()
    video_mix = models.PositiveSmallIntegerField(default = 100)

    class Meta:
        verbose_name = u'Plantilla Fondo-Diapositiva-Vídeo'

    def __unicode__(self):
        return self.nombre

class Video(models.Model):
    VIDEO_STATUS = (
        ('INC', 'Incompleto'),
        ('PTE', 'Pendiente'),
        ('PRO', 'Procesando'),
        ('LIS', 'Listo'),
        ('APR', 'Aprobado'),
        ('REC', 'Rechazado')
    )

    fichero = models.CharField(max_length = 255, editable = False) # En el futuro tal vez sea models.FilePathField
    status = models.CharField(max_length = 3, choices = VIDEO_STATUS, editable = False, default = 'INC')
    plantilla = models.ForeignKey(PlantillaFDV, null = True, blank = True)

 
    ## Metadata
    titulo = models.CharField(max_length = 30)
    observacion = models.TextField(null = True, blank = True)
    fecha_grabacion = models.DateTimeField(auto_now_add = True)
    autor = models.CharField(max_length = 30)
    email = models.EmailField()

    def __unicode__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        if self.fichero:
            utils.remove_file_path(self.fichero)
        super(Video, self).delete(*args, **kwargs)

class FicheroEntrada(models.Model):
    video = models.ForeignKey(Video, editable = False)
    tipo = models.ForeignKey(TipoVideo, editable = False, null = True)
    fichero = models.CharField(max_length = 255)

class TecData(models.Model):
    audio_bitrate = models.FloatField(null = True)
    audio_channels = models.CharField(max_length = 20, null = True)
    audio_codec = models.CharField(max_length = 10, null = True)
    audio_rate = models.PositiveIntegerField(null = True)
    bitrate = models.PositiveIntegerField(null = True)
    duration = models.FloatField(null = True)
    format = models.CharField(max_length = 30, null = True)
    size = models.PositiveIntegerField(null = True)
    video_bitrate = models.FloatField(null = True)
    video_codec = models.CharField(max_length = 10, null = True)
    video_color = models.CharField(max_length = 10, null = True)
    video_height = models.PositiveIntegerField(null = True)
    video_rate = models.FloatField(null = True)
    video_wh_ratio = models.FloatField(null = True)
    video_width = models.PositiveIntegerField(null = True)

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
        ('HEC', 'Hecho')
    )

    QUEUE_TYPE = (
        ('COP', u'Copia'),
        ('PIL', u'Píldora'),
        ('PRE', u'Previsualización')
    )

    objects = ColaManager()

    video = models.ForeignKey(Video)
    status = models.CharField(max_length = 3, choices = QUEUE_STATUS, default = 'PEN')
    tipo = models.CharField(max_length = 3, choices = QUEUE_TYPE)
    comienzo = models.DateTimeField(null = True, blank = True)
    fin = models.DateTimeField(null = True, blank = True)
    logfile = models.FileField(upload_to = "logs", null = True, blank = True)

    def __unicode__(self):
       return dict(self.QUEUE_TYPE)[self.tipo] + ": " + self.video.__unicode__()

    class Meta:
        verbose_name = u'tarea'
        verbose_name_plural = u'tareas'
