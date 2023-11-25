import os
from PIL import Image, ImageDraw
from django.conf import settings
from .models import DataModel

def add_frame_to_image(image, coordinates, path):
    try:
        draw = ImageDraw.Draw(image)

        draw.rectangle([coordinates["left"], coordinates["top"], coordinates["right"], coordinates["bottom"]],
                        outline="red",
                        width=3)

        image = image.convert('RGB')
        temp_image_path = "temp.jpg"
        image.save(temp_image_path, 'JPEG')

        image_instance = DataModel()
        with open(temp_image_path, 'rb') as f:
            image_instance.file.save(f'{path}.jpg', f)
        image_instance.save()


        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        return True

    except Exception as e:
        print(f"Błąd: {e}")
        return False
