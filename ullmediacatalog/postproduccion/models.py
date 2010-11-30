#encoding: utf-8
from django.db import models

# Create your models here.

class TipoVideo(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

class PlantillaFDV(models.Model):   # (Fondo-Disapositiva-Video)
    nombre = models.CharField(max_length=50)

    fondo = models.ImageField(upload_to='plantillas')

    diapositiva_tipo = models.ForeignKey(TipoVideo, related_name="t_diap")
    diapositiva_x = models.PositiveSmallIntegerField()
    diapositiva_y = models.PositiveSmallIntegerField()
    diapositiva_ancho = models.PositiveSmallIntegerField()
    diapositiva_alto = models.PositiveSmallIntegerField()
    diapositiva_mix = models.PositiveSmallIntegerField(default=100)

    video_tipo = models.ForeignKey(TipoVideo, related_name="t_vid")
    video_x = models.PositiveSmallIntegerField()
    video_y = models.PositiveSmallIntegerField()
    video_ancho = models.PositiveSmallIntegerField()
    video_alto = models.PositiveSmallIntegerField()
    video_mix = models.PositiveSmallIntegerField(default=100)

    class Meta:
        verbose_name = u'Plantilla Fondo-Diapositiva-Vídeo'

    def __unicode__(self):
        return self.nombre

class Video(models.Model):
    VIDEO_STATUS = (
        ('PTE', 'Pendiente'),
        ('PRO', 'Procesando'),
        ('LIS', 'Listo'),
        ('APR', 'Aprobado'),
        ('REC', 'Rechazado')
    )

    fichero = models.CharField(max_length=255) # En el futuro tal vez sea models.FilePathField
    status = models.CharField(max_length=3, choices=VIDEO_STATUS)
    plantilla = models.ForeignKey(PlantillaFDV, null=True, blank=True)

    ## Metadata
    titulo = models.CharField(max_length=30)
    descripcion = models.TextField()
    autor = models.CharField(max_length=30)
    email = models.EmailField()

    def __unicode__(self):
        return self.titulo

class FicheroEntrada(models.Model):
    video = models.ForeignKey(Video)
    tipo = models.ForeignKey(TipoVideo)
    fichero = models.CharField(max_length=255)

## COLA ##

class ColaManager(models.Manager):
    """
    Devuelve el número de trabajos que están siendo codificados en este momento.
    """
    def count_actives(self):
        return super(ColaManager, self).get_query_set().filter(status='PRO').count()

    """
    Devuelve la lista ordenada de vídeos encolados pendientes de ser codificados.
    """
    def get_next_pending(self):
         return super(ColaManager, self).get_query_set().filter(status='PEN').order_by('id')[0]

class Cola(models.Model):
    QUEUE_STATUS = (
        ('PEN', 'Pendiente'),
        ('PRO', 'Procesando'),
        ('HEC', 'Hecho')
    )

    QUEUE_TYPE = (
        ('PIL', 'Píldora'),
        ('PRE', 'Previsualización')
    )

    objects = ColaManager()

    video = models.ForeignKey(Video)
    status = models.CharField(max_length = 3, choices = QUEUE_STATUS, default = 'PEN')
    tipo = models.CharField(max_length = 3, choices = QUEUE_TYPE)
    comienzo = models.DateTimeField(null = True, blank = True)
    fin = models.DateTimeField(null = True, blank = True)
    logfile = models.FileField(upload_to = "logs", null = True, blank = True)

    def __unicode__(self):
       return self.video.__unicode__()

    class Meta:
        verbose_name = u'tarea'
        verbose_name_plural = u'tareas'
