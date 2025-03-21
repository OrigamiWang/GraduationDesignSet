from flask import Flask

from handler import *
from util import standard_response


app = Flask(__name__)

# 获取模型列表
@app.route("/sd/get_model_list", methods=['GET', 'POST'])
@standard_response
def get_model_list():
    return get_model_list_handler()

@app.route("/sd/get_model_img_list", methods=["POST"])
@standard_response
def get_model_img_list():
    req = request.get_json()
    buk, path = req['buk'], req['path']
    return get_model_imgs_handler(buk, path)


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
    uid = request.args.get('uid')
    file = request.files.get('file')
    filename = file.filename
    return upload_file_handler(uid, filename, file)

@app.route("/file/upload/check", methods=['POST'])
@standard_response
def check_avatar_file():
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

# 用户操作
@app.route("/user/register", methods=["POST"])
@standard_response
def register():
    req = request.get_json()
    name = req['username']
    pswd = req['password']
    return create_user_handler(name, pswd)

@app.route("/user/one", methods=["POST"])
@standard_response
def get_one_user():
    req = request.get_json()
    name = req['username']
    return get_one_user_hanlder(name)

@app.route("/user/check", methods=["POST"])
@standard_response
def check_user():
    req = request.get_json()
    name = req['username']
    pswd = req['password']
    return check_user_handler(name, pswd)

# history
@app.route("/history/add", methods=["POST"])
@standard_response
def add_his():
    req = request.get_json()
    uid, type_name, buk, filepath = req['uid'], req['type'], req['buk'], req['filepath']
    config, input = req.get('config', {}), req.get('input', {})
    add_his_handler(uid, type_name, buk, filepath, config, input)

@app.route("/history/all", methods=["POST"])
@standard_response
def get_all_his():
    req = request.get_json()
    uid = req['uid']
    return get_all_his_handler(uid)

@app.route("/history/other", methods=["POST"])
@standard_response
def get_other_his():
    req = request.get_json()
    uid = req['uid']
    return get_other_his_handler(uid)


@app.route("/oss/path", methods=["POST"])
@standard_response
def get_img_url_by_path():
    req = request.get_json()
    path = req['path']
    return get_oss_url_by_path_handler(path)

@app.route("/file/uploadB64", methods=["POST"])
def upload_base64_file():
    req = request.get_json()
    uid = req['uid']
    filename = req['filename']
    base64_data = req['base64_data']
    type_name = req['type_name']
    return upload_b64file_handler(uid, filename, type_name, base64_data)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


