from dal import user


def get_one_user_hanlder(name):
    return user.select_one_user(name)

def create_user_handler(name, pswd):
    user_list = get_one_user_hanlder(name)
    if len(user_list) > 0:
        return {"code": -1, "msg": "用户名已存在!"}
    user.insert_user(name, pswd)
    res = get_one_user_hanlder(name)[0]
    res['code'] = 0
    return res

def check_user_handler(name, pswd):
    return user.check_user_existance(name, pswd)