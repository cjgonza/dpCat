from django.contrib import admin
from postproduccion.models import Cola, Video, FicheroEntrada, TipoVideo, PlantillaFDV, MetadataOA, MetadataGen, InformeProduccion, RegistroPublicacion

class FicherosInline(admin.StackedInline):
    model = FicheroEntrada
    max_num = 2
    extra = 1

class MetadataOAInline(admin.StackedInline):
    model = MetadataOA
    max_num = 1

class MetadataGenInline(admin.StackedInline):
    model = MetadataGen
    max_num = 1

class InformeProduccionInline(admin.StackedInline):
    model = InformeProduccion
    max_num = 1

class ColaInline(admin.TabularInline):
    model = Cola
    max_num = 1
    readonly_fields = ('status', 'tipo', 'comienzo', 'fin', 'logfile')

class RegistroPublicacionInline(admin.TabularInline):
    model = RegistroPublicacion
    max_num = 1
    readonly_fields = ('enlace',)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status')
    inlines = [FicherosInline, MetadataOAInline, MetadataGenInline, InformeProduccionInline, ColaInline, RegistroPublicacionInline]
    list_filter = ('status', 'objecto_aprendizaje')

class TipoVideoInline(admin.StackedInline):
    model = TipoVideo
    extra = 1

class PlantillaFDVAdmin(admin.ModelAdmin):
    inlines = [TipoVideoInline]

admin.site.register(PlantillaFDV, PlantillaFDVAdmin)
admin.site.register(Video, VideoAdmin)
