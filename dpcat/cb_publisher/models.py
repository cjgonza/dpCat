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
