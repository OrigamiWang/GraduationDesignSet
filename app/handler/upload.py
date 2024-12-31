import base64
from util import forward_img

def upload_file_handler(filename, img_file):
    base64_data = base64.b64encode(img_file.read())
    base64_str = str(base64_data, 'utf-8')
    return {
        "filename": filename,
        "base64_str": base64_str
    }

def check_human_img_handler(filename, img_file):
    res = forward_img('POST', 'http://127.0.0.1:4000/infer/check_avatar', files={'file':  (filename, img_file.read())})
    return res.json()
