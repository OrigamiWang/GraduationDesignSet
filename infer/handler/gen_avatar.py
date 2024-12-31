from biz import human_face_detect


def check_avatar_handler(file):
    res = {
        "code": 0,
        "msg": "",
        "res": None
    }

    img_data = file.read()
    # 检测图片合法性
    human_detect_res = human_face_detect(img_data)
    print(f'human_detect_res: {human_detect_res}')
    if len(human_detect_res) == 0:
        res["code"] = -1
        res["msg"] = "图片中没有人，或者人脸被遮挡"
    elif len(human_detect_res) > 1:
        res["code"] = -1
        res["msg"] = "图片中有多个人存在"
    else:
        res["msg"] = "图片合法"
    return res