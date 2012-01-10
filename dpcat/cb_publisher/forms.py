#encoding: utf-8
from django import forms
from cb_publisher.functions import get_categories

class ConfigForm(forms.Form):
    clipbucket_url = forms.CharField(label = u'URL del sitio Clipbucket')
    username = forms.CharField(label = u'Usuario del Clipbucket para subida de vídeos')
    password = forms.CharField(label = u'Contraseña del Clipbucket para subida de vídeos', widget = forms.PasswordInput)
    local_dir = forms.CharField(label = u'Directorio local de intercambio de ficheros (SAMBA, NFS, ...)')
    remote_dir = forms.CharField(label = u'Directorio remoto de intercambio de ficheros (SAMBA, NFS, ...)')
