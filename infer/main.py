from flask import Flask, request

from common import PORT
from model import *
from handler import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

#  生成图片，并返回图片的base64编码
@app.route("/infer/txt2img", methods=['POST'])
def txt2img():
    b64_imgs = txt2img_handler(request.get_json())
    return b64_imgs


# 生成头像, 先检测图片合法性(多人/非人都是无效，只能是单人)
@app.route("/infer/check_avatar", methods=['POST'])
def detect_human():
    print(request.files)
    file = request.files['file']
    print(file)
    return check_avatar_handler(file)





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
