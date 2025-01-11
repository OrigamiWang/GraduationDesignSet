import base64
from util import forward_img, MINIO_CLI
import time
from datetime import datetime

def upload_file_handler(uid, filename, img_file):
    base64_data = base64.b64encode(img_file.read())
    base64_str = str(base64_data, 'utf-8')

    ts = int(time.time() * 1000)
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    d = f'{year}{month}{day}'
    dst = f'user-{uid}/{d}/{ts}_{filename}' 

    presigned_url = MINIO_CLI.upload_file("stable-diffusion", dst, base64_data)

    return {
        "filename": filename,
        "base64_str": base64_str,
        "oss_url": presigned_url
    }

def upload_b64file_handler(uid, filename, type_name, base64_str):
    print("base64_str: ", len(base64_str))
    base64_data = base64_str.encode('utf-8')

    ts = int(time.time() * 1000)
    dst = f'user-{uid}/{type_name}/{ts}_{filename}' 

    presigned_url = MINIO_CLI.upload_file("stable-diffusion", dst, base64_data)

    return {
        "filename": filename,
        "base64_str": base64_str,
        "oss_url": presigned_url
    }


def check_human_img_handler(filename, img_file):
    res = forward_img('POST', 'http://127.0.0.1:4000/infer/check_avatar', files={'file':  (filename, img_file.read())})
    return res.json()
