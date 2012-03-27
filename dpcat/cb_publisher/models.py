# -*- encoding: utf-8 -*-

from django.db import models

from postproduccion.models import Video

class PublicacionManager(models.Manager):
    """
    Devuelve la lista de publicaciones pendientes de ser publicadas.
    """
    def get_pendings(self):
        return super(PublicacionManager, self).get_query_set().filter(status = 'PEN').order_by('id')
    
    """
    Devuelve la lista de publicaciones erroneas.
    """
    def get_failed(self):
        return super(PublicacionManager, self).get_query_set().filter(status = 'ERR')


class Publicacion(models.Model):
    QUEUE_STATUS = (
        ('PEN', 'Pendiente'),
        ('EXE', u'En ejecución'),
        ('ERR', 'Error'),
    )

    objects = PublicacionManager()

    video = models.ForeignKey(Video)
    status = models.CharField(max_length = 3, choices = QUEUE_STATUS, default = 'PEN')
    logfile = models.FileField(upload_to = "logs", null = True, blank = True)
    data = models.TextField()

    class Meta:
        verbose_name = u'publicación'
        verbose_name_plural = u'publicaciones'

    def __unicode__(self):
        return self.video.titulo

    def set_status(self, st):
        self.status = st
        self.save()

class RegistroPublicacion(models.Model):
    video = models.ForeignKey(Video)
    fecha = models.DateTimeField(auto_now_add = True)
    enlace = models.CharField(max_length = 255)

    class Meta:
        verbose_name = u'registro de publicación'
        verbose_name_plural = u'registro de publicaciones'
