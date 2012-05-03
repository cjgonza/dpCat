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
    license = forms.ChoiceField(choices = Metadata.LICENSE_KEYS, label = u'Licencia de uso')
    category = forms.TypedChoiceField(label = u'Categoría de publicación', coerce = int)
    collection = forms.TypedChoiceField(
        label = u'Colección',
        choices = ((0, 'Sin colección'), (1, u'Añadir a existente'), (2, u'Crear nueva')),
        initial = 0,
        widget = forms.RadioSelect,
        coerce = int,
    )

class AddToCollectionForm(forms.Form):
    add_to_collection = forms.TypedChoiceField(label = u'Colección', coerce = int)

class NewCollectionForm(forms.Form):
    new_collection_name = forms.CharField(label = 'Nombre de la colección')
    new_collection_description = forms.CharField(label = u'Descripción de la colección', widget = forms.Textarea)
    new_collection_tags = forms.CharField(label = u'Etiquetas de la colección')
    new_collection_category = forms.TypedChoiceField(label = u'Categoría de la colección', coerce = int)
