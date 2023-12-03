from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import DataModel
from .utils import add_frame_to_image
from manage import MODEL
from model.utils import predict
from datetime import datetime
from PIL import Image

def index(request):
    context = {}
    return render(request, "main/main_page.html", context)

def model(request):
    timestamp = datetime.now().strftime('%m%d%Y%h%m%S')
    uploaded_images = []

    if request.method == 'POST':
        files = request.FILES.getlist('file')  # Zmiana na getlist, aby obsłużyć listę plików

        for uploaded_image in files:
            image = Image.open(BytesIO(uploaded_image.read()))
            uploaded_images.append(image)

    for i, uploaded_image in enumerate(uploaded_images):
        coordinates = predict(MODEL, uploaded_image)
        # coordinates = { 'left': 50, 'right': 100, 'bottom': 100, 'top': 50}

        processed_image = add_frame_to_image(uploaded_image, coordinates, f'{timestamp}_{i}')

    context = {'MEDIA_URL': settings.MEDIA_URL, 'file_paths': [f'{timestamp}_{i}.jpg' for i in range(len(uploaded_images))]}
    return render(request, "main/predict_page.html", context)