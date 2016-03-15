#coding: utf-8
from django.db import models

# Create your models here.

class Settings(models.Model):
    clave = models.CharField(max_length=30, unique=True)
    valor = models.TextField()

    class Meta:
        verbose_name = u'configuración'
        verbose_name_plural = u'configuraciones'

    def __unicode__(self):
        return self.clave

