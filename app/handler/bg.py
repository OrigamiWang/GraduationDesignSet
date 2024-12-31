from util import forward



def bg_replace_handler(src_img, bg_img):
    res = forward('POST', 'http://127.0.0.1:6000/bg/replace', data={"src_img": src_img, "bg_img": bg_img})
    return res.json()['res']