from django.contrib import admin
from configuracion.models import Settings


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('clave', 'valor')

admin.site.register(Settings, SettingsAdmin)
