from django.forms import ModelForm
from postproduccion.models import Video, FicheroEntrada

class VideoForm(ModelForm):
    class Meta:
        model = Video

class FicheroEntradaForm(ModelForm):
    class Meta:
        model = FicheroEntrada
