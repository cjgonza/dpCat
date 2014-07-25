# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from postproduccion.models import Video
from postproduccion.video import generate_tecdata
from postproduccion.encoder import is_video_file
import shutil


class Command(BaseCommand):
    args = u'video_id filename'
    help = u'Reemplaza el vídeo de una producción.'

    def handle(self, *args, **options):

        # Validación de los argumentos
        if len(args) != 2:
            print "Error: Número de parámetros incorrecto."
            return
        v_id, filename = args
        try:
            v = Video.objects.get(id=v_id)
        except Video.DoesNotExist:
            print "Error: El video #%s no existe" % v_id
            return
        if not is_video_file(filename):
            print "Error: '%s' no es un fichero de vídeo válido." % filename
            return

        print "* Reemplazando el vídeo de la producción '%s':" % v
        print " - Creando copia de seguridad..."
        bak = v.fichero + ".bak"
        shutil.move(v.fichero, bak)
        print " - Copiando nuevo vídeo..."
        shutil.copy(filename, v.fichero)
        print " - Regenerando metadata técnica..."
        generate_tecdata(v)
        print "Hecho."
