#encoding: utf-8
from django import forms
from django.forms import ModelForm, CharField, Textarea, widgets, Form
from django.forms.models import BaseInlineFormSet
from postproduccion.models import Video, FicheroEntrada, Metadata, InformeProduccion, IncidenciaProduccion
from postproduccion.utils import is_exec, is_dir

class VideoForm(ModelForm):
    class Meta:
        model = Video

class InformeCreacionForm(ModelForm):
    class Meta:
        model = InformeProduccion
        fields = ('observacion', 'aprobacion', 'fecha_grabacion')

class IncidenciaProduccionForm(ModelForm):
    comentario = CharField(required = True, widget = Textarea())

    class Meta:
        model = IncidenciaProduccion
        fields = ('comentario',)

class FicheroEntradaForm(ModelForm):
    class Meta:
        model = FicheroEntrada

class RequiredBaseInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredBaseInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class MetadataForm(ModelForm):
    class Meta:
        model = Metadata

class ASCIIField(forms.CharField):
    def validate(self, value):
        super(ASCIIField, self).validate(value)
        try:
            str(value)
        except UnicodeEncodeError:
            raise forms.ValidationError("El campo no debe contener tíldes ni caracteres especiales")

class ExecutableField(ASCIIField):
    def validate(self, value):
        super(ExecutableField, self).validate(value)
        if not is_exec(value):
            raise forms.ValidationError("El fichero no existe o no es ejecutable")

class DirectoryField(ASCIIField):
    def validate(self, value):
        super(DirectoryField, self).validate(value)
        if not is_dir(value):
            raise forms.ValidationError("El directorio no existe o no es accesible")

class ConfigForm(Form):
    max_encoding_tasks = forms.IntegerField(label = u'Nº máximo de codificaciones simultaneas')
    mediainfo_path = ExecutableField(label = u'Ruta del \'mediainfo\'')
    melt_path = ExecutableField(label = u'Ruta del \'melt\'')
    ffmpeg_path = ExecutableField(label = u'Ruta del \'ffmpeg\'')
    crontab_path = ExecutableField(label = u'Ruta del \'crontab\'')
    max_preview_width = forms.IntegerField(label = u'Anchura máxima de la previsualización')
    max_preview_height = forms.IntegerField(label = u'Altura máxima de la previsualización')
    video_library_path = DirectoryField(label = u'Directorio base de la videoteca')
    video_input_path = DirectoryField(label = u'Directorio base de los ficheros de vídeo fuente')
    previews_path = DirectoryField(label = u'Directorio de base de las previsualizaciones')
    token_valid_days = forms.IntegerField(label = u'Periodo de validez del ticket de usuario (en días)')
    site_url = forms.CharField(label = u'URL del sitio')
    log_max_lines = forms.IntegerField(label = u'Nº máximo de líneas del registro de sistema')
    max_num_logfiles = forms.IntegerField(label = u'Nº máximo de ficheros de registro de sistema antiguos')
    return_email = forms.EmailField(label = u'Dirección del remitente para envíos de correos electrónicos')
    
