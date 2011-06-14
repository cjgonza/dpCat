#encoding: utf-8
from django import forms
from cb_publisher.functions import get_categories

class ConfigForm(forms.Form):
    php_path = forms.CharField(label = u'Ruta de la intérprete PHP (php-cli)')
    clipbucket_path = forms.CharField(label = u'Ruta de la instalación del Clipbucket')
    username = forms.CharField(label = u'Usuario del Clipbucket para subida de vídeos')
    password = forms.CharField(label = u'Contraseña del Clipbucket para subida de vídeos', widget = forms.PasswordInput)

class PublishingForm(forms.Form):
    category = forms.ChoiceField(choices = get_categories(), label = u'Categoría de publicación')
