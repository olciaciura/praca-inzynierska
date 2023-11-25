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
    max_height = 223
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
    # img = Image.open(path_to_image)
    # device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    img, left_margin, top_margin = preprocess(img)
    print(left_margin, top_margin)
    model.eval()
    with torch.no_grad():
        prediction = model([img])
    print(prediction)
# bierzemy ten bb z najwiekszym scorem
    scores_tensor = prediction[0]['scores']
    print(scores_tensor)
    # best_score_id = torch.argmax(scores_tensor)
    best_score_id = 0
    bb = prediction[0]['boxes'][best_score_id]
    coordinates = { 'left':     bb[0] - left_margin,
                    'right':    bb[2] - left_margin,
                    'bottom':   bb[3] - top_margin,
                    'top':      bb[1] - top_margin}

    return coordinates

if __name__ == '__main__':
    model = load_model('model.p')
    print(type(model))
