# -*- encoding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from cb_publisher.models import Publicacion
from cb_publisher.functions import publish
import threading

class Command(NoArgsCommand):
    help = 'Publica los videos pendientes en la cola'

    def handle_noargs(self, **options):

        while True:
            threads = []
            pub_pendings = list(Publicacion.objects.get_pendings())
            if len(pub_pendings) and not Publicacion.objects.is_processing():
                t = pub_pendings[0]
                t.set_status('EXE')
                th = threading.Thread(target = publish, kwargs = {'task' : t})
                th.start()
                threads.append(th)

            for th in threads:
                th.join()

            # Si no hay trabajos esperando o está lleno el cupo de trabajos en proceso, salimos.
            if (not Publicacion.objects.count_pendings() or Publicacion.objects.is_processing()):
                break
