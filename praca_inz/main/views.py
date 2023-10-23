from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.


# klasa ImageUploadView - w tym metoda get - pobieranie zdjecia, post - przetworzenie zdjecia i wysłanie z ramką
#tu tez może być model jako funkcja globalna

def index(request):
    context = {}
    return render(request, "main/main_page.html", context)

def model(request):
    context = {}
    return render(request, "main/empty.html", context)
