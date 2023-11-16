# przetwarzanie obrazów przed analizą przez AI




import logging

import numpy as np
from PIL import Image

from src.api.utils import is_json_valid
from src.models.utils import decode_image

logger = logging.getLogger(__name__)


def rel_to_abs_bb(im_shape: tuple, bbox: tuple) -> tuple:
    """Convert relative values of bounding boxes (ranged from 0 to 1) to absolute, based on image dims.

    Args:
        im_shape (tuple): Context image shape in format (im_w, im_h, im_c).
        bbox (tuple): tuple of four floats ranged from 0 to 1, representing coordinates of two bbox corners.
            bbox format is compatible with PyTorch object detection models.

    Returns:
        tuple: tuple of four floats ranged from 0 to corresponding im_shape.
    """
    im_h, im_w, _ = im_shape
    y1, x1, y2, x2 = bbox
    return round(y1 * im_h), round(x1 * im_w), round(y2 * im_h), round(x2 * im_w)


def get_bb_size(y1: int, x1: int, y2: int, x2: int) -> tuple:
    """Calculate bbox width, and height.

    Returns:
        tuple: (bbox width, bbox height)
    Raises:
        ValueError: when x1 is greater than x2 or y1 is greater than y2
    """
    if x1 > x2 or y1 > y2:
        raise ValueError(f'x2 and y2 must be greater than x1 nad y1.')
    bb_w = x2 - x1
    bb_h = y2 - y1
    return bb_w, bb_h


def add_margin(pil_img, top, right, bottom, left):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    color = (0, 0, 0)
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def resize_with_padding(new_size: tuple, image: Image) -> Image:
    desired_w, desired_h = new_size
    old_w, old_h = image.size
    top_pad = (desired_h - old_h) // 2
    bottom_pad = desired_h - old_h - top_pad
    right_pad = (desired_w - old_w) // 2
    left_pad = desired_w - old_w - right_pad
    return add_margin(image, top_pad, right_pad, bottom_pad, left_pad)


def get_cropped_image_size(image_size: tuple, bbox: tuple):
    img_w, img_h, bb_w, bb_h, w_ratio, h_ratio = get_image_stats(image_size, bbox)
    if w_ratio < h_ratio:
        new_h = round(img_w * bb_h / bb_w)
        new_w = img_w
    else:
        new_h = img_h
        new_w = round(img_h * bb_w / bb_h)
    return new_h, new_w


def get_image_stats(image_size, bboxes):
    img_w, img_h = image_size
    bb_w, bb_h = get_bb_size(*bboxes)
    w_ratio = img_w / bb_w
    h_ratio = img_h / bb_h
    return img_w, img_h, bb_w, bb_h, w_ratio, h_ratio


def add_bbox_rel_padding(bboxes, rel_padding):
    """Add relative padding that scales to bbox size.

    Args:
        bboxes (tuple): bbox with relative values.
        rel_padding (float): Positive number used to calculate padding,
            if image_shape is (1000, 1000, 3) and rel_padding is 0.1, then bbox width and height will increase
            by 2*1000*0.1

    Returns:
        np.ndarray: bbox with padding added, and values clipped to image size.
    """
    return np.array([-1, -1, 1, 1]) * rel_padding + bboxes


def strip_and_resize_image(image: Image.Image, rel_bbox: tuple, rel_padding: float):
    """Extract bounding box interior from image, center it, add padding that scales to bbox size
    and resize extracted image to maximally fill original image, but with image shape ratio kept.

    Args:
        image (Image): Pil image with tree channels. Base for extraction.
        rel_bbox (tuple): Relative coordinates of two bounding box corners. Image will be striped to this bbox interior.
        rel_padding (float, optional): Percentage of image that will be added to bbox to extend it. Defaults to 0.

    Returns:
        Image: Pil image with the same dims, as original one, but only with a content from bbox. Content is centered, but not scaled.
    """
    rel_bbox = add_bbox_rel_padding(rel_bbox, rel_padding)
    bbox = rel_to_abs_bb(image.size + (3,), rel_bbox)
    cropped_image = image.crop(bbox)
    new_h, new_w = get_cropped_image_size(image.size, bbox)
    new_image = cropped_image.resize((new_h, new_w))
    return resize_with_padding(image.size, new_image)


class Preprocessor:
    """Class responsible for image preprocessing before prediction.

    Args:
        image_base64 (str): Image in base64 format which we want to send to model.
        bbox_dict (dict): Dictionary with four keys ("xmax", "xmin", "ymax", "ymin")
                                    with coordinates of bounding box on image.

    Attributes:
        image (Image): Image in format easy to process it.
        bbox (list): List with boudning box coordinates in order: 'xmin', 'ymin', 'xmax', 'ymax'.
    """

    def __init__(self, image_base64, bbox_dict):
        self.image = decode_image(image_base64)
        self.prepare_bbox(bbox_dict)

    def prepare_bbox(self, bbox_dict):
        """Method which prepares list with bounding box coordinates from dictionary and saves it to class attributes.

        Args:
            bbox_dict (dict): Dictionary with four keys ("xmax", "xmin", "ymax", "ymin")
                                    with coordinates of bounding box on image.
        """
        if not is_json_valid(bbox_dict, "xmin", "ymin", "xmax", "ymax"):
            self.bbox = [0, 0, 1, 1]
            logger.warning(
                "Dictionary with bounding box coordinates isn't valid, they were set to default"
            )
        self.bbox = [
            bbox_dict["xmin"],
            bbox_dict["ymin"],
            bbox_dict["xmax"],
            bbox_dict["ymax"],
        ]

    def preprocess(self, rel_padding=0.1):
        """Method which, based on bounding box coordinates (class attribute), crops image and returns it with black color outside the bounding box.
        We can also set how much of the picture we want to see outside the bounding box using rel_padding argument.

        Args:
            rel_padding (float, optional): Relative padding - how much of the picture we want to see outside the bounding box. Defaults to 0.1.

        Returns:
            Image: Preprocessed image ready to prediction.
        """
        if self.image is not None:
            return strip_and_resize_image(self.image, self.bbox, rel_padding)
