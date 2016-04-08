# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Sum
from postproduccion.models import Video, TecData
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

        tecdata = TecData.objects.filter(video=qs).aggregate(Sum('duration'))
        if tecdata['duration__sum'] is None:
            d = 0
        else:
            d = timedelta(seconds = tecdata['duration__sum'])

        print(u"Producciones realizadas: %s (%s)" % (str(qs.count()), d))

        # Producciones validadas

        tecdata = TecData.objects.filter(video=qs.filter(status='LIS')).aggregate(Sum('duration'))
        if tecdata['duration__sum'] is None:
            d = 0
        else:
            d = timedelta(seconds = tecdata['duration__sum'])

        print(u"Producciones validadas: %s (%s)" % (str(qs.filter(status='LIS').count()), d))

        # Píldoras

        tecdata = TecData.objects.filter(video=qs.exclude(plantilla=None)).aggregate(Sum('duration'))
        if tecdata['duration__sum'] is None:
            d = 0
        else:
            d = timedelta(seconds = tecdata['duration__sum'])

        print(u"Píldoras: %s (%s)" % (str(qs.exclude(plantilla=None).count()), d))

        # Producciones propias

        tecdata = TecData.objects.filter(video=qs.filter(plantilla=None)).aggregate(Sum('duration'))
        if tecdata['duration__sum'] is None:
            d = 0
        else:
            d = timedelta(seconds = tecdata['duration__sum'])

        print(u"Producciones propias: %s (%s)" % (str(qs.filter(plantilla=None).count()), d))
