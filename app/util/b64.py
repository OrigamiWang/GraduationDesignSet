import base64

"""
    对图片进行base64加解密
"""
def encode_base64(img):
    with open(img, mode='rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)
        base64_str = str(base64_data, 'utf-8')
        return base64_str

def decode_base64(base64_str):
    return base64.b64decode(base64_str) # <class 'bytes'>

# base64_str = encode_base64('testdata/test.jpg')
# with open('img_base64.txt', mode='w') as f:
#     f.write(base64_str)
# decode_base64(base64_str)
