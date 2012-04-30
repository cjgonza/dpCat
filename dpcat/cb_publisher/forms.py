#encoding: utf-8
from django import forms
from cb_publisher.functions import get_categories
from postproduccion.models import Metadata

class ConfigForm(forms.Form):
    clipbucket_url = forms.CharField(label = u'URL del sitio Clipbucket')
    username = forms.CharField(label = u'Usuario del Clipbucket para subida de vídeos')
    password = forms.CharField(label = u'Contraseña del Clipbucket para subida de vídeos', widget = forms.PasswordInput)
    local_dir = forms.CharField(label = u'Directorio local de intercambio de ficheros (SAMBA, NFS, ...)')
    remote_dir = forms.CharField(label = u'Directorio remoto de intercambio de ficheros (SAMBA, NFS, ...)')

class PublishingForm(forms.Form):
    title = forms.CharField(max_length = 255, label = u'Título')
    description = forms.CharField(label = u'Descripción', widget = forms.Textarea)
    tags = forms.CharField(max_length = 255, label = u'Etiquetas')
    license = forms.ChoiceField(label = u'Licencia de uso')
    category = forms.ChoiceField(label = u'Categoría de publicación')
