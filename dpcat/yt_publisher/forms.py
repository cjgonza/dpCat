#encoding: utf-8
from django import forms

class ConfigForm(forms.Form):
    client_id = forms.CharField(label = u'API Client ID')
    client_secret = forms.CharField(label = u'API Client Secret')
    max_tasks = forms.IntegerField(label = u'Nº máximo de publicaciones simultaneas')

class PublishingForm(forms.Form):
    title = forms.CharField(max_length = 255, label = u'Título')
    description = forms.CharField(label = u'Descripción', widget = forms.Textarea)
    tags = forms.CharField(max_length = 255, label = u'Etiquetas')
    playlist = forms.TypedChoiceField(
        label = u'Lista de reproducción',
        choices = ((0, 'Sin lista de reproducción'), (1, u'Añadir a existente'), (2, u'Crear nueva')),
        initial = 0,
        widget = forms.RadioSelect,
        coerce = int,
    )

class AddToPlaylistForm(forms.Form):
    add_to_playlist = forms.TypedChoiceField(label = u'Lista de reproducción')

class NewPlaylistForm(forms.Form):
    new_playlist_name = forms.CharField(label = 'Nombre de la lista de reproducción')
    new_playlist_description = forms.CharField(label = u'Descripción de la lista de reproducción', widget = forms.Textarea)
