#encoding: utf-8
from django import forms

class ConfigForm(forms.Form):
    client_id = forms.CharField(label = u'API Client ID')
    client_secret = forms.CharField(label = u'API Client Secret')
