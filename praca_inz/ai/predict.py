import logging
import os
from datetime import datetime

import numpy as np
import tensorflow as tf
from onnxruntime.capi.onnxruntime_pybind11_state import NoSuchFile

from config import config
from src.helpers.errors import log_exception_with_error
from src.models.load import load_object
from src.models.onnx_models import BoundingBoxModel
from src.models.utils import decode_image

logger = logging.getLogger(__name__)


class Predictor:
    """Class responsible for prediction.

    Args:
        model_name (str): Name of model which we want to use for prediction.
        classificator_name (str): Name of classifier which we want to use for classification.

    Attributes:
        model (Sequential): Stored model for predictions.
        clf (NearestCentroidWithProbas): Stored classifier for classifications.
    """    
    def __init__(self, model_name, classificator_name, BB_predictor_name):

        self.load_model(model_name)
        self.load_classificator(classificator_name)
        self.load_BB_predictor(BB_predictor_name)

    def load_model(self, model_name):
        """Method which loads model from right path.

        Args:
            model_name (str): Name of model which we want to load.
        """        
        path = os.path.join(config.MODELS_PATH_LOCAL, model_name)
        try:
            self.model = tf.keras.models.load_model(path, compile=False)
        except OSError as error:
            date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            log_exception_with_error(
                error, f"{date} Error loading model: {model_name}, path: {path}"
            )
            self.model = None

    def load_classificator(self, classificator_name):
        """Method which loads classifier from the right path.

        Args:
            classificator_name (str): Name of classifier which we want to load (with .pklx suffix).
        """        
        path = os.path.join(config.MODELS_PATH_LOCAL, classificator_name)
        try:
            self.clf = load_object(path)
        except FileNotFoundError as error:
            date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            log_exception_with_error(
                error,
                f"{date} Error loading classificator: {classificator_name}, path: {path}",
            )
            self.clf = None

    def load_BB_predictor(self , BB_predictor_name):
        """Method which loads BB predictor from the right path.

        Args:
            BB_predictor_name (BoundingBoxModel): Name of model which we want to load (with .onnx suffix).
        """        
        path = os.path.join(config.MODELS_PATH_LOCAL, BB_predictor_name)
        try:
            self.BB_predictor = BoundingBoxModel(path)
        except FileNotFoundError:
            date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(
                f"{date} Error loading BB predictor: {BB_predictor_name}, path: {path}"
            )
            self.BB_predictor = None

    def predict_embedding(self, image):
        """Method which for given image returns embedding.

        Args:
            image_base64 (str): Image in base64 format.

        Returns:
            ndarray: Embedding of given image.
        """        
        if image is not None:
            image = image.resize((224, 224))
            image = np.reshape(np.array(image), (1, 224, 224, 3))
            if self.model is not None:
                return self.model.predict(np.array(image), verbose=0)
            else:
                return None
        else:
            logger.warning("Image is None, something went wrong while decoding.")
            image = None
        if (self.model is not None) and (image is not None):
            return self.model.predict(np.array(image), verbose=0)
        else:
            logger.warning("Not enough resources to predict embedding")
            return None

    def classify(self, embedding, k):
        """Method which for given embedding classifies k possible parts.

        Args:
            embedding (ndarray): Embedding of image.
            k (int): Number of predictions which we want to return.

        Returns:
            list: List of ids of predicted parts.
        """
        if (embedding is not None) and (self.clf is not None):
            prediction = self.clf.predict_multiple_(embedding, k)
            if (
                isinstance(prediction, tuple)
                and len(prediction) == 2
                and isinstance(prediction[1], np.ndarray)
                and len(prediction[1]) == 1
                and isinstance(prediction[1][0], np.ndarray)
            ):
                return list(prediction[1][0])
            else:
                logger.warning("Prediction structure isn't valid, check it")
                return []
        else:
            logger.warning("Embedding is None or there is no classifier, so it is not possible to classify")
            return []

    def predict_BB(self, image_base64):
        """Method which for given image finds object on it and returns bounding box.

        Args:
            image_base64 (str): Image in base64 format.

        Returns:
            tuple: bounding box coordinates (xmin, ymin, xmax, ymax).
        """        
        image = decode_image(image_base64)
        if image is not None:
            if self.BB_predictor is not None:
                return self.BB_predictor.get_bounding_box(image)
            else:
                return None
        else:
            date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            logger.error(
                f"{date} (predict_BB) Bad image format, should be base64"
            )
            return None


if __name__ == "__main__":
    path = os.path.join("..", "..", "tests", "test_data", "expected_result_BlobDB.txt")
    with open(path, "rb") as f:
        image_base64 = f.read()
    predictor = Predictor(image_base64, "test_encoder", "classificator.pkl")
    print(predictor.classify(5))
