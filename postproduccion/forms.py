#encoding: utf-8
from django import forms
from django.forms import ModelForm, CharField, Textarea, widgets, Form, ValidationError
from django.forms.models import BaseInlineFormSet
from django.template import Template, TemplateSyntaxError
from postproduccion.models import Video, FicheroEntrada, MetadataOA, MetadataGen, InformeProduccion, IncidenciaProduccion
from postproduccion.utils import is_exec, is_dir
from postproduccion.encoder import is_video_file
from configuracion import config
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

import os
class LoginForm(AuthenticationForm):
    def clean(self):
        username = password= None
        if 'username' in self.cleaned_data.keys():
            username = self.cleaned_data['username']
        if 'password'  in self.cleaned_data.keys():
            password = self.cleaned_data['password']
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError('Error de login')
        return self.cleaned_data
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control'})

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['plantilla'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['titulo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['autor'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tipoVideo'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['objecto_aprendizaje'].widget.attrs.update({'class' : 'minimal', 'checked' : 'checked'})

class InformeCreacionForm(ModelForm):
    class Meta:
        model = InformeProduccion
        fields = ('observacion', 'aprobacion', 'fecha_grabacion')
    def __init__(self, *args, **kwargs):
        super(InformeCreacionForm, self).__init__(*args, **kwargs)
        self.fields['observacion'].widget.attrs.update({'class' : 'form-control', 'rows' : '5'})
        self.fields['aprobacion'].widget.attrs.update({'class' : 'minimal', 'checked' : 'checked'})
        self.fields['fecha_grabacion'].widget.attrs.update({'class' : 'form-control pull-right'})

class VideoEditarForm(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        exclude = ['plantilla']
        #fields = ('titulo', 'autor', 'email', 'objecto_aprendizaje')
    def __init__(self, *args, **kwargs):
        super(VideoEditarForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['autor'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tipoVideo'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['objecto_aprendizaje'].widget.attrs.update({'class' : 'minimal', 'checked' : 'checked'})

class InformeEditarForm(ModelForm):
    class Meta:
        model = InformeProduccion
        fields = ('observacion',)
    def __init__(self, *args, **kwargs):
        super(InformeEditarForm, self).__init__(*args, **kwargs)
        self.fields['observacion'].widget.attrs.update({'class' : 'form-control', 'rows' : '5'})

class IncidenciaProduccionForm(ModelForm):
    class Meta:
        model = IncidenciaProduccion
        fields = ('comentario',)
    def __init__(self, *args, **kwargs):
        super(IncidenciaProduccionForm, self).__init__(*args, **kwargs)
        self.fields['comentario'].widget.attrs.update({'class' : 'form-control', 'rows' : '5'})

class FicheroEntradaForm(ModelForm):
    class Meta:
        model = FicheroEntrada
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(FicheroEntradaForm, self).__init__(*args, **kwargs)
        self.fields['fichero'].widget.attrs.update({'class' : 'form-control'})

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
    def __init__(self, *args, **kwargs):
        super(MetadataOAForm, self).__init__(*args, **kwargs)
        self.fields['knowledge_areas'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        self.fields['creator'].widget.attrs.update({'class' : 'form-control'})
        self.fields['keyword'].widget.attrs.update({'class' : 'form-control'})
        self.fields['description'].widget.attrs.update({'class' : 'form-control', 'rows' : '5'})
        self.fields['license'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['guideline'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['contributor'].widget.attrs.update({'class' : 'form-control'})
        self.fields['audience'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['typical_age_range'].widget.attrs.update({'class' : 'form-control'})
        self.fields['source'].widget.attrs.update({'class' : 'form-control'})
        self.fields['language'].widget.attrs.update({'class' : 'form-control'})
        self.fields['ispartof'].widget.attrs.update({'class' : 'form-control'})
        self.fields['location'].widget.attrs.update({'class' : 'form-control'})
        self.fields['venue'].widget.attrs.update({'class' : 'form-control'})
        self.fields['temporal'].widget.attrs.update({'class' : 'form-control', 'rows' : '5'})
        self.fields['rightsholder'].widget.attrs.update({'class' : 'form-control'})
        self.fields['type'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['interactivity_type'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['interactivity_level'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['learning_resource_type'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['semantic_density'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['context'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['dificulty'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['typical_learning_time'].widget.attrs.update({'class' : 'form-control'})
        self.fields['educational_language'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['purpose'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['unesco'].widget.attrs.update({'class' : 'form-control select2'})

class MetadataGenForm(ModelForm):
    class Meta:
        model = MetadataGen
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(MetadataGenForm, self).__init__(*args, **kwargs)
        self.fields['knowledge_areas'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        self.fields['creator'].widget.attrs.update({'class' : 'form-control'})
        self.fields['keyword'].widget.attrs.update({'class' : 'form-control'})
        self.fields['description'].widget.attrs.update({'class' : 'form-control', 'rows' : '5'})
        self.fields['license'].widget.attrs.update({'class' : 'form-control select2'})
        self.fields['transcription'].widget.attrs.update({'class' : 'form-control', 'rows' : '5'})
        self.fields['contributor'].widget.attrs.update({'class' : 'form-control'})
        self.fields['language'].widget.attrs.update({'class' : 'form-control'})
        self.fields['location'].widget.attrs.update({'class' : 'form-control'})
        self.fields['venue'].widget.attrs.update({'class' : 'form-control'})

class ASCIIField(forms.CharField):
    def validate(self, value):
        super(ASCIIField, self).validate(value)
        try:
            str(value)
        except UnicodeEncodeError:
            raise forms.ValidationError("El campo no debe contener tíldes ni caracteres especiales.")

class ExecutableField(ASCIIField):
    def validate(self, value):
        super(ExecutableField, self).validate(value)
        if not is_exec(value):
            raise forms.ValidationError("El fichero no existe o no es ejecutable.")

class DirectoryField(ASCIIField):
    def validate(self, value):
        super(DirectoryField, self).validate(value)
        if not is_dir(value):
            raise forms.ValidationError("El directorio no existe o no es accesible.")

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

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

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

    def __init__(self, *args, **kwargs):
        super(ConfigMailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})