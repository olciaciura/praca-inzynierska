from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import DataModel
from .utils import draw_frame_on_image, clear_media_folder

# Create your views here.

# klasa ImageUploadView - w tym metoda get - pobieranie zdjecia, post - przetworzenie zdjecia i wysłanie z ramką
#tu tez może być model jako funkcja globalna

def index(request):
    context = {}
    return render(request, "main/main_page.html", context)

def model(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['file']

        clear_media_folder()
        new_entry = DataModel(file=uploaded_image)
        new_entry.save()

    last_entry = DataModel.objects.last()

# TODO: należy coordynaty policzyc z modelu a nie podać z ręki

    coordinates = { 'left':     50,
                    'right':    100,
                    'bottom':   100,
                    'top':      50}

    draw_frame_on_image(last_entry.file if last_entry else None, coordinates)

    context = { 'MEDIA_URL': settings.MEDIA_URL }
    return render(request, "main/predict_page.html", context)
