from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.


# klasa ImageUploadView - w tym metoda get - pobieranie zdjecia, post - przetworzenie zdjecia i wysłanie z ramką

def index(request):
    context = {}
    return render(request, "main/main_page.html", context)
