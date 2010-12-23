from django.contrib import admin
from postproduccion.models import Cola, Video, FicheroEntrada, TipoVideo, PlantillaFDV, TecData

class ColaAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'tipo', 'status', 'comienzo', 'fin', 'logfile')

class FicherosInline(admin.StackedInline):
    model = FicheroEntrada
    extra = 1

class TecDataInline(admin.StackedInline):
    model = TecData
    max_num = 1

class VideoAdmin(admin.ModelAdmin):
    inlines = [FicherosInline, TecDataInline]

class PlantillaFDVAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'fondo']}),
        ('Diapositiva', {'fields': ['diapositiva_tipo', 'diapositiva_x', 'diapositiva_y', 'diapositiva_ancho', 'diapositiva_alto', 'diapositiva_mix']}),
        ('Video', {'fields': ['video_tipo', 'video_x', 'video_y', 'video_ancho', 'video_alto', 'video_mix']}),
    ]

admin.site.register(Cola, ColaAdmin)
admin.site.register(PlantillaFDV, PlantillaFDVAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(TipoVideo)
