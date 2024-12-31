import io
from PIL import Image
from io import BytesIO
import base64

from .b64 import decode_base64

def b64_2_img(b64_str: str):
    if b64_str.find(",") != -1:
        b64_str = b64_str.split(",")[1]
    b64_byte = decode_base64(b64_str)
    img_stream = io.BytesIO(b64_byte)
    img = Image.open(img_stream)
    return img


# Convert Image to Base64 
def img_2_b64(image):
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    buff = BytesIO()
    image.save(buff, format="JPEG")
    img_bytes = base64.b64encode(buff.getvalue())
    img_str = img_bytes.decode('utf-8')
    return img_str