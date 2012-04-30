# -*- encoding: utf-8 -*-

from django.db import models

from postproduccion.models import Video

class Publicacion(models.Model):
    QUEUE_STATUS = (
        ('PEN', 'Pendiente'),
        ('EXE', u'En ejecución'),
        ('ERR', 'Error'),
    )

    video = models.ForeignKey(Video)
    status = models.CharField(max_length = 3, choices = QUEUE_STATUS, default = 'PEN')
    logfile = models.FileField(upload_to = "logs", null = True, blank = True)
    data = models.TextField()

    class Meta:
        verbose_name = u'publicación'
        verbose_name_plural = u'publicaciones'

    def __unicode__(self):
        return self.video.titulo

class RegistroPublicacion(models.Model):
    video = models.ForeignKey(Video)
    fecha = models.DateTimeField(auto_now_add = True)
    enlace = models.CharField(max_length = 255)

    class Meta:
        verbose_name = u'registro de publicación'
        verbose_name_plural = u'registro de publicaciones'
