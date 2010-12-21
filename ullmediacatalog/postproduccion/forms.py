from django.forms import ModelForm
from postproduccion.models import Video

class VideoForm(ModelForm):
    class Meta:
        model = Video
