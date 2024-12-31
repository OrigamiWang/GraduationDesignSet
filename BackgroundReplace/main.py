from flask import Flask, request

from service.replace_bg_service import replace_bg, get_mask
from util.img import b64_2_img, img_2_b64

app = Flask(__name__)


@app.route("/bg/replace", methods=['POST'])
def replace_bg_img():
    req = request.get_json()
    src_img = b64_2_img(req['src_img'])
    bg_img = b64_2_img(req['bg_img'])
    output_image = get_mask(src_img)
    new_img = replace_bg(output_image, bg_img)
    return {
        "res": img_2_b64(new_img)
    }



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
