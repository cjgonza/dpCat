from django.forms import ModelForm, BooleanField, Select
from django.forms.models import BaseInlineFormSet
from postproduccion.models import Video, FicheroEntrada, Metadata, InformeProduccion

class VideoForm(ModelForm):
    class Meta:
        model = Video

class InformeCreacionForm(ModelForm):
    class Meta:
        model = InformeProduccion
        fields = ('observacion', 'aprobacion')

class InformeAprobacionForm(ModelForm):
    class Meta:
        model = InformeProduccion
        fields = ('aprobado', 'comentario')

class FicheroEntradaForm(ModelForm):
    class Meta:
        model = FicheroEntrada

class RequiredBaseInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredBaseInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class MetadataForm(ModelForm):
    class Meta:
        model = Metadata
