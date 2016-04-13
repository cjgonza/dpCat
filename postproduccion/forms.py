#encoding: utf-8
from django import forms
from django.forms import ModelForm, CharField, Textarea, widgets, Form, ValidationError
from django.forms.models import BaseInlineFormSet
from django.template import Template, TemplateSyntaxError
from postproduccion.models import Video, FicheroEntrada, MetadataOA, MetadataGen, InformeProduccion, IncidenciaProduccion
from postproduccion.utils import is_exec, is_dir
from postproduccion.encoder import is_video_file
from configuracion import config
import os

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

class InformeCreacionForm(ModelForm):
    class Meta:
        model = InformeProduccion
        fields = ('observacion', 'aprobacion', 'fecha_grabacion')

class VideoEditarForm(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        exclude = ['plantilla']
        #fields = ('titulo', 'autor', 'email', 'objecto_aprendizaje')

class InformeEditarForm(ModelForm):
    class Meta:
        model = InformeProduccion
        fields = ('observacion',)

class IncidenciaProduccionForm(ModelForm):
    comentario = CharField(required = True, widget = Textarea())

    class Meta:
        model = IncidenciaProduccion
        fields = ('comentario',)

class FicheroEntradaForm(ModelForm):
    class Meta:
        model = FicheroEntrada
        fields = '__all__'

    def clean_fichero(self):
        data = self.cleaned_data['fichero']
        try:
            str(data)
        except UnicodeEncodeError:
            raise forms.ValidationError("El campo no debe contener tíldes ni caracteres especiales")
        if not is_video_file(os.path.normpath(config.get_option('VIDEO_INPUT_PATH') + data)):
            raise ValidationError(u"El fichero no es un formato de vídeo reconocido")
        return data

class RequiredBaseInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredBaseInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class MetadataOAForm(ModelForm):
    class Meta:
        model = MetadataOA
        fields = '__all__'

class MetadataGenForm(ModelForm):
    class Meta:
        model = MetadataGen
        fields = '__all__'

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

class TemplateField(forms.CharField):
    widget = Textarea()
    def validate(self, value):
        super(TemplateField, self).validate(value)
        try:
            Template(value)
        except:
            raise forms.ValidationError(u"El mensaje contiene etiquetas inválidas")

class ConfigForm(Form):
    max_encoding_tasks = forms.IntegerField(label = u'Nº máximo de codificaciones simultaneas')
    mediainfo_path = ExecutableField(label = u'Ruta del \'mediainfo\'')
    melt_path = ExecutableField(label = u'Ruta del \'melt\'')
    avconv_path = ExecutableField(label = u'Ruta del \'avconv\'')
    mp4box_path = ExecutableField(label = u'Ruta del \'MP4Box\'')
    exiftool_path = ExecutableField(label = u'Ruta del \'exiftool\'')
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

class ConfigMailForm(Form):
    return_email = forms.EmailField(label = u'Dirección del remitente para envíos de correos electrónicos')
    notify_mail_subject = forms.CharField(label = u'Asunto del correo de notificación de producción realizada')
    notify_mail_message = TemplateField(label = u'Mensaje del correo de notificación de producción realizada')
    custom_mail_subject = forms.CharField(label = u'Asusnto del correo de nuevo ticket por parte del operador')
    custom_mail_message = TemplateField(label = u'Mensaje del correo de nuevo ticket por parte del operador')
    validated_mail_subject = forms.CharField(label = u'Asunto del correo de aviso de validación de una producción')
    validated_mail_message = TemplateField(label = u'Mensaje del correo de aviso de validación de una producción')
    published_mail_subject = forms.CharField(label = u'Asunto del correo de aviso de publicación de una producción')
    published_mail_message = TemplateField(label = u'Mensaje del correo de aviso de publicación de una producción')
