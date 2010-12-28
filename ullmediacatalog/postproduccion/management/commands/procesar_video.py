from django.core.management.base import NoArgsCommand
from ullmediacatalog.postproduccion.models import Cola
from ullmediacatalog.postproduccion.queue import process_task
from ullmediacatalog.configuracion.config import get_option
import threading

class Command(NoArgsCommand):
    help = 'Procesa los videos pendientes en la cola'

    def handle_noargs(self, **options):

        while True:
            threads = []
            for t in Cola.objects.get_pendings():
                if get_option('MAX_ENCODING_TASKS') > Cola.objects.count_actives():
                    th = threading.Thread(target = process_task, kwargs = {'task' : t})
                    th.start()
                    threads.append(th)
                else:
                    break

            for th in threads:
                th.join()

            if not Cola.objects.count_pendings():
                break
