#coding: utf-8
from django import forms
from django.forms.widgets import RadioFieldRenderer

class ConfigForm(forms.Form):
    client_id = forms.CharField(label = u'API Client ID')
    client_secret = forms.CharField(label = u'API Client Secret')
    max_tasks = forms.IntegerField(label = u'Nº máximo de publicaciones simultaneas')

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})
################################################
class MyRadioFieldRenderer(RadioFieldRenderer):
    outer_html = '{content}'
    inner_html = '<div>{choice_value}{sub_widgets}</div>'

class MyRadioSelect(forms.RadioSelect):
    renderer = MyRadioFieldRenderer
################################################
class PublishingForm(forms.Form):
    title = forms.CharField(max_length = 100, label = u'Título')
    description = forms.CharField(max_length = 5000, label = u'Descripción', widget = forms.Textarea)
    tags = forms.CharField(max_length = 255, label = u'Etiquetas')
    playlist = forms.TypedChoiceField(
        label = u'Lista de reproducción',
        choices = ((0, 'Sin lista de reproduccion'), (1, u'Anadir a existente'), (2, u'Crear nueva')),
        initial = 0,
        widget = MyRadioSelect(attrs={
            'class': 'minimal'}),
        coerce = int,
    )
    title.widget.attrs.update({'class' : 'form-control'})
    description.widget.attrs.update({'class' : 'form-control'})
    tags.widget.attrs.update({'class' : 'form-control'})

class AddToPlaylistForm(forms.Form):
    add_to_playlist = forms.TypedChoiceField(label = u'Lista de reproducción')
    add_to_playlist.widget.attrs.update({'class' : 'form-control select2'})

class NewPlaylistForm(forms.Form):
    new_playlist_name = forms.CharField(label = u'Nombre de la lista de reproducción')
    new_playlist_description = forms.CharField(label = u'Descripción de la lista de reproducción', widget = forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(NewPlaylistForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})