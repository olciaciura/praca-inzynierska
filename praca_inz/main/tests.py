import pickle
from django.test import TestCase
from model.utils import preprocess, predict
import torch
from PIL import Image
import timeit

class YourModelTestCase(TestCase):

    def setUp(self):
        # Tutaj możesz umieścić kod do inicjalizacji modelu przed testami, jeśli jest to potrzebne
        # Na przykład, wczytaj model za pomocą torch.load() lub utwórz go od nowa

        # Przykładowe wczytywanie modelu - dostosuj do swojego przypadku
        with open('./model/model.p', 'rb') as f:
            self.model = pickle.load(f)
        self.model.eval()

    def test_preprocess_function(self):
        img_path = './model/photos/test/15.jpg'
        img = Image.open(img_path)

        preprocessed_img, left_margin, top_margin = preprocess(img)

        expected_left_margin = 2
        expected_top_margin = 0

        self.assertEqual(left_margin, expected_left_margin)
        self.assertEqual(top_margin, expected_top_margin)

    def test_predict_function(self):
        img_path = './model/photos/test/15.jpg'
        img = Image.open(img_path)

        coordinates = predict(self.model, img)
        expected_coordinates = {'left': torch.tensor(63.8811), 
                                'right': torch.tensor(125.6562), 
                                'bottom': torch.tensor(110.4140), 
                                'top': torch.tensor(62.7198)}

        torch.testing.assert_close(coordinates['top'], expected_coordinates['top'], rtol=1e-03, atol=1e-08)
        torch.testing.assert_close(coordinates['bottom'], expected_coordinates['bottom'], rtol=1e-05, atol=1e-08)
        torch.testing.assert_close(coordinates['left'], expected_coordinates['left'], rtol=1e-05, atol=1e-08)
        torch.testing.assert_close(coordinates['right'], expected_coordinates['right'], rtol=1e-05, atol=1e-08)

    

    def test_predict_function_speed(self):
        img_path = './model/photos/test/15.jpg'
        img = Image.open(img_path)

        execution_time = timeit.timeit(lambda: predict(self.model, img), number=1000)
        print(f"Execution time: {execution_time} seconds")

