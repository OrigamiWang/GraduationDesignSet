from flask import Flask

from handler import *
from util import standard_response


app = Flask(__name__)

# 获取模型列表
@app.route("/sd/get_model_list", methods=['GET', 'POST'])
@standard_response
def get_model_list():
    return get_model_list_handler()


# 基于base获取lora列表
@app.route("/sd/get_lora_list_by_base_name", methods=['POST'])
@standard_response
def get_lora_list_by_base_name():
    return get_lora_list_by_base_name_handler()

# generate
@app.route("/sd/get_vae_list_by_base_name", methods=['POST'])
@standard_response
def get_vae_list_by_base_name():
    return get_vae_list_by_base_name_handler()

# generate
@app.route("/sd/get_style_list", methods=['POST'])
@standard_response
def get_style_list():
    return get_style_list_handler()

# generate
@app.route("/infer/generate", methods=['POST'])
@standard_response
def generate():
    return generate_handler()


@app.route("/manage/user_permissions", methods=['GET'])
@standard_response
def get_user_permissions():
    return get_user_permissions_handler()

# 获取home页面下的权限列表
@app.route("/manage/home_permissions", methods=['GET'])
@standard_response
def get_home_permissions():
    return get_home_permissions_handler()

@app.route("/file/upload", methods=['POST'])
@standard_response
def upload_file():
    file = request.files.get('file')
    filename = file.filename
    return upload_file_handler(filename, file)

@app.route("/file/upload/check", methods=['POST'])
@standard_response
def check_avatar_file():
    print(request.files)
    file = request.files.get('file')
    filename = file.filename
    return check_human_img_handler(filename, file)

@app.route("/bg/replace", methods=["POST"])
@standard_response
def background_replace():
    req = request.get_json()
    src_img = req['src_img']
    bg_img = req['bg_img']
    return bg_replace_handler(src_img, bg_img)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
