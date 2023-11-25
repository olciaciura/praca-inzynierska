from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import DataModel
from .utils import draw_frame_on_image, clear_media_folder
from manage import MODEL
from model.utils import predict
from datetime import datetime
from PIL import Image

def index(request):
    context = {}
    return render(request, "main/main_page.html", context)

def model(request):
    timestamp = datetime.now().strftime('%m%d%Y%h%m%S')
    print(timestamp)

    if request.method == 'POST':
        uploaded_image = request.FILES['file']
        uploaded_image = Image.open(BytesIO(uploaded_image.read()))

    coordinates = predict(MODEL, uploaded_image)
    # coordinates = { 'left':     50,
    #                 'right':    100,
    #                 'bottom':   100,
    #                 'top':      50}

    draw_frame_on_image(uploaded_image, coordinates, timestamp)

    context = { 'MEDIA_URL': settings.MEDIA_URL, 'file_path': f'{timestamp}.jpg' }
    return render(request, "main/predict_page.html", context)
