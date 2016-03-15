# -*- encoding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from postproduccion.models import Cola
from postproduccion.queue import process_task, available_slots
import threading

class Command(NoArgsCommand):
    help = 'Procesa los videos pendientes en la cola'

    def handle_noargs(self, **options):

        while True:
            threads = []
            pendings = list(Cola.objects.get_pendings())
            for t in pendings:
                if available_slots():
                    t.set_status('PRO')
                    th = threading.Thread(target = process_task, kwargs = {'task' : t})
                    th.start()
                    threads.append(th)
                else:
                    break

            for th in threads:
                th.join()

            # Si no hay trabajos esperando o está lleno el cupo de trabajos en proceso, salimos.
            if (not Cola.objects.count_pendings() or not available_slots()):
                break
