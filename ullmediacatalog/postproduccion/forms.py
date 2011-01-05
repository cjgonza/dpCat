from django.forms import ModelForm
from django.forms.models import BaseModelFormSet
from postproduccion.models import Video, FicheroEntrada

class VideoForm(ModelForm):
    class Meta:
        model = Video

class FicheroEntradaForm(ModelForm):
    class Meta:
        model = FicheroEntrada

class RequiredBaseModelFormSet(BaseModelFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredBaseModelFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form
