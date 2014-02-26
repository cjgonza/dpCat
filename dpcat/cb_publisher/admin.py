from django.contrib import admin
from cb_publisher.models import Publicacion, RegistroPublicacionCB

class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('video', 'status')

class RegistroPublicacionAdmin(admin.ModelAdmin):
    list_display = ('video', 'fecha', 'enlace')

admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(RegistroPublicacionCB, RegistroPublicacionAdmin)

