from configuracion.models import Settings


def set_option(c, v):
    try:
        s = Settings.objects.get(clave=c)
        s.valor = v
    except Settings.DoesNotExist:
        s = Settings(clave=c, valor=v)
    s.save()


def get_option(c):
    try:
        return Settings.objects.get(clave=c).valor
    except Settings.DoesNotExist:
        return None


def del_option(c):
    try:
        Settings.objects.get(clave=c).delete()
        return True
    except Settings.DoesNotExist:
        return False


def list_options():
    return [s.clave for s in Settings.objects.all()]
