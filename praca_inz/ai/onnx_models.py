import onnxruntime
from typing import Union, Optional, Tuple
from pathlib import Path
from PIL import ImageOps
from PIL.Image import Image
import numpy as np
from onnxruntime.capi.onnxruntime_pybind11_state import RuntimeException


class EmbeddingModel:
    """
    A class that loads specified onnx model used for making embeddings. It uses onnxruntime module.

    Args:
        model_path (Union[Path, str]) - path to the file with onnx model.
        default_resize (Optional[Tuple[int, int]]) - the size input photo should be resized to if the onnx model
        does not have that information. If onnx model requires a specific input shape this argument is ignored
        and the photo is resized to the parameters given by the model. Defaults to (500, 500).
    """
    def __init__(self, model_path: Union[Path, str], default_resize: Optional[Tuple[int, int]] = (500, 500)):
        onnx_model_path = str(model_path) if isinstance(model_path, Path) else model_path
        self.sess_options = onnxruntime.SessionOptions()
        # self.sess_options.intra_op_num_threads = 4
        self.sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_PARALLEL
        self.sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.model = onnxruntime.InferenceSession(onnx_model_path, sess_options=self.sess_options)
        _, self.im_w, self.im_h, _ = self.model.get_inputs()[0].shape
        if not isinstance(self.im_w, int):
            self.im_w = default_resize[0]
        if not isinstance(self.im_h, int):
            self.im_h = default_resize[1]

    def get_embedding(self, image: Image) -> np.ndarray:
        """
        A method that takes an image and returns its embedding.

        Args:
            image (Image): image of which embedding you want to get.
        Returns:
            Embedding of the given photo in a form of a numpy array.
        """
        image = image.resize((self.im_w, self.im_h)).convert('RGB')
        image = ImageOps.exif_transpose(image)
        image = np.asarray(image, dtype=np.float32).reshape((1, self.im_w, self.im_h, 3))
        ort_inputs = {self.model.get_inputs()[0].name: image}
        embedding = self.model.run(None, ort_inputs)
        return embedding


class BoundingBoxModel:
    """
    A class that loads specified onnx model used for predicting bounding boxes. It uses onnxruntime module.

    Args:
        model_path (Union[Path, str]): path to the file with onnx model.
    """
    def __init__(self, model_path: Union[Path, str]):
        onnx_model_path = str(model_path) if isinstance(model_path, Path) else model_path
        self.sess_options = onnxruntime.SessionOptions()
        # self.sess_options.intra_op_num_threads = 4
        self.sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_PARALLEL
        self.sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.model = onnxruntime.InferenceSession(onnx_model_path, sess_options=self.sess_options)
        _, _, self.im_w, self.im_h = self.model.get_inputs()[0].shape

    def get_bounding_box(self, image: Image) -> Optional[Tuple[float, float, float, float]]:
        """
        A method that returns a bounding box of the object in the picture. If no object is found returns None.
        Coordinates (xmin, ymin, xmax, ymax) values refer to the percentage of the image height and width.

        Args:
            image (Image): image with an object of which bounding box you want to get.
        Returns:
            Optional[Tuple[float, float, float, float]]: bounding box coordinates (xmin, ymin, xmax, ymax) in picture
             width and height percentage.
        """
        image = image.resize((self.im_w, self.im_h)).convert('RGB')
        image = ImageOps.exif_transpose(image)
        image = np.asarray(image, dtype=np.float32).transpose(2, 0, 1).reshape((1, 3, self.im_w, self.im_h)) / 255
        image = image.astype(np.float32)
        ort_inputs = {self.model.get_inputs()[0].name: image}
        try:
            bb, *scores_and_classes = self.model.run(None, ort_inputs)
        except RuntimeException as e:
            return None
        if scores_and_classes[0].dtype in [np.int32, np.int64, np.int16]:
            classes, scores = scores_and_classes
        else:
            scores, classes = scores_and_classes
        index = scores.argmax()
        bb = bb[index]
        x1, y1, x2, y2 = bb
        return x1 / self.im_w, y1 / self.im_h, x2 / self.im_w, y2 / self.im_h


