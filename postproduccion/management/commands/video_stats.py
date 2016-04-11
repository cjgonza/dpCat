# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from postproduccion.models import Video, TecData
from postproduccion impot video

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
        d = video.get_duration(qs)
        print(u"Producciones realizadas: %s (%s)" % (str(qs.count()), d))

        # Producciones validadas
        d = video.get_duration(qs.filter(status='LIS'))
        print(u"Producciones validadas: %s (%s)" % (str(qs.filter(status='LIS').count()), d))

        # Píldoras
        d = video.get_duration(qs.exclude(plantilla=None))
        print(u"Píldoras: %s (%s)" % (str(qs.exclude(plantilla=None).count()), d))

        # Producciones propias
        d = video.get_duration(qs.filter(plantilla=None))
        print(u"Producciones propias: %s (%s)" % (str(qs.filter(plantilla=None).count()), d))
