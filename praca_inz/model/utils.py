import pickle
from PIL import Image
import math
import os
from torchvision import transforms
import torch

compose = transforms.Compose([
    transforms.PILToTensor(),
    transforms.ConvertImageDtype(torch.float)
])

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def preprocess(image):
    max_height = 225
    max_width = 227
    w, h = image.size

    left_margin = (max_width - w)//2
    top_margin = (max_height - h)//2
    image = add_margin(image, top_margin, left_margin, math.ceil((max_height - h)/2), math.ceil((max_width - w)/2), (0,0,0))
    image = compose(image)

    return image, left_margin, top_margin

def load_model(path_to_model):
    with open(path_to_model, 'rb') as f:
        model = pickle.load(f)
    return model

def predict(model, img):
    img, left_margin, top_margin = preprocess(img)
    model.eval()
    with torch.no_grad():
        prediction = model([img])
    if(len(prediction[0]['boxes'])!=0):
        bb = prediction[0]['boxes'][0]
        coordinates = { 'left':     bb[0] - left_margin,
                        'right':    bb[2] - left_margin,
                        'bottom':   bb[3] - top_margin,
                        'top':      bb[1] - top_margin}
    else:
        coordinates = { 'left':     0,
                        'right':    0,
                        'bottom':   0,
                        'top':      0}

    return coordinates
