from django.core.management.base import NoArgsCommand
from ullmediacatalog.postproduccion.models import Cola
from ullmediacatalog.postproduccion.queue import process_task
from ullmediacatalog.configuracion.config import get_option

class Command(NoArgsCommand):
    help = 'Procesa el siguiente video en la cola'

    def handle_noargs(self, **options):

        if get_option('MAX_ENCODING_TASKS') > Cola.objects.count_actives():
            process_task(Cola.objects.get_next_pending())
