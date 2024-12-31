import io
from PIL import Image

from .b64 import decode_base64

def b64_to_img(b64_str):
    b64_byte = decode_base64(b64_str)
    img_stream = io.BytesIO(b64_byte)
    img = Image.open(img_stream)
    return img
