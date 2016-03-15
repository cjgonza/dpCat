# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from postproduccion.models import Video
from datetime import timedelta

class Command(BaseCommand):
    args = u'[año]'
    help = u'Muestra las estadísticas de vídeos.'

    def handle(self, *args, **options):

        # Validación de los argumentos
        if len(args) > 1:
            print "Error: Número de parámetros incorrecto."
            return
        if len(args) == 1:
            (year,) = args
            try:
                int(year)
            except ValueError:
                print "Error: El argumento debe ser un año en formato numérico"
                return
            qs = Video.objects.filter(informeproduccion__fecha_produccion__year = year)
        else:
            qs = Video.objects.all()

        # Producciones realizadas

        d = timedelta()
        for v in qs:
            if hasattr(v, 'tecdata'):
                d += timedelta(seconds = v.tecdata.duration)

        print(u"Producciones realizadas: %s (%s)" % (str(qs.count()), d))

        # Producciones validadas

        d = timedelta()
        for v in qs.filter(status='LIS'):
            if hasattr(v, 'tecdata'):
                d += timedelta(seconds = v.tecdata.duration)

        print(u"Producciones validadas: %s (%s)" % (str(qs.filter(status='LIS').count()), d))


        # Píldoras

        d = timedelta()
        for v in qs.exclude(plantilla=None):
            if hasattr(v, 'tecdata'):
                d += timedelta(seconds = v.tecdata.duration)

        print(u"Píldoras: %s (%s)" % (str(qs.exclude(plantilla=None).count()), d))

        # Producciones propias

        d = timedelta()
        for v in qs.filter(plantilla=None):
            if hasattr(v, 'tecdata'):
                d += timedelta(seconds = v.tecdata.duration)

        print(u"Producciones propias: %s (%s)" % (str(qs.filter(plantilla=None).count()), d))


