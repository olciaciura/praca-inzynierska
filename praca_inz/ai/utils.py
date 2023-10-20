#komunikacja z modelem AI
# tu powinna byś load_model i predict???


import base64
import binascii
import datetime
import io
import zipfile

from PIL import Image, UnidentifiedImageError

from src.helpers.errors import log_exception_with_error


def unzip_model(file_path, extract_path):
    """Function which unpacks model from .zip file to given directory.

    Args:
        file_path (str): Path to .zip file.
        extract_path (str): Path to directory where we want to unpack .zip file.
    """
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def decode_image(image_base64):
    """Function which decodes image from base64 format and returns it as an image.

    Args:
        image_base64 (str): Image in base64 format.

    Returns:
        JpegImageFile: Image file.
    """
    try:
        base64_decoded = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(base64_decoded))
    except (binascii.Error, ValueError, UnidentifiedImageError) as error:
        date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        log_exception_with_error(error, f"{date} (predict_embedding) Bad image format, should be base64")
        image = None
    return image
