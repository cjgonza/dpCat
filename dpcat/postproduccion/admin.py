from django.contrib import admin
from postproduccion.models import Cola, Video, FicheroEntrada, TipoVideo, PlantillaFDV, TecData, Metadata, InformeProduccion

class ColaAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'tipo', 'status', 'comienzo', 'fin', 'logfile')

class FicherosInline(admin.StackedInline):
    model = FicheroEntrada
    extra = 1

class TecDataInline(admin.StackedInline):
    model = TecData
    max_num = 1
 
class MetadataInline(admin.StackedInline):
    model = Metadata
    max_num = 1

class InformeProduccionInline(admin.StackedInline):
    model = InformeProduccion
    max_num = 1

class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status')
    inlines = [FicherosInline, TecDataInline, MetadataInline, InformeProduccionInline]
    actions = ['custom_delete_selected']

    def custom_delete_selected(self, request, queryset):
        for obj in queryset:
            if hasattr(obj, 'previsualizacion'):
                obj.previsualizacion.delete()
            obj.delete()

    custom_delete_selected.short_description = "Borrar videos y ficheros (sin confirmacion)"

class TipoVideoInline(admin.StackedInline):
    model = TipoVideo
    extra = 1

class PlantillaFDVAdmin(admin.ModelAdmin):
    inlines = [TipoVideoInline]

admin.site.register(Cola, ColaAdmin)
admin.site.register(PlantillaFDV, PlantillaFDVAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(TipoVideo)
admin.site.register(Metadata)
