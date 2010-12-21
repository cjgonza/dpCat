# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

#from postrpoduccion.models import Video
from postproduccion.forms import VideoForm
from postproduccion import utils

def crear(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            v = form.save(commit=False)
            v.fichero = utils.generate_safe_filename(v.titulo, 'mp4')
            v.save()
            return HttpResponse("Ok")
    else:
        form = VideoForm()
    return render_to_response("postproduccion/crear.html", { 'form' : form }, context_instance=RequestContext(request))

