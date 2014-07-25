from django.contrib import admin
from yt_publisher.models import Publicacion

class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('video', 'status')

admin.site.register(Publicacion, PublicacionAdmin)
