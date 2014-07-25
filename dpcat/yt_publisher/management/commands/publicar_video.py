# -*- encoding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from yt_publisher.models import Publicacion
from yt_publisher.upload import publish
from yt_publisher.functions import available_slots
import threading
import logging

class Command(NoArgsCommand):
    help = 'Publica los videos pendientes en la cola'

    def handle_noargs(self, **options):
        logging.basicConfig()

        while True:
            threads = []
            pendings = list(Publicacion.objects.get_pendings())
            for t in pendings:
                if available_slots():
                    t.set_status('EXE')
                    th = threading.Thread(target = publish, kwargs = {'task' : t})
                    th.start()
                    threads.append(th)
                else:
                    break

            for th in threads:
                th.join()

            # Si no hay trabajos esperando o está lleno el cupo de trabajos en proceso, salimos.
            if (not Publicacion.objects.count_pendings() or not available_slots()):
                break
