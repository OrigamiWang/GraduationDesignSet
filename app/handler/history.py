from dal import add_his, select_all, select_other



def add_his_handler(uid, type_name, buk, filepath, config, input):
    add_his(uid, type_name, buk, filepath, config, input)

def get_all_his_handler(uid):
    return select_all(uid)

def get_other_his_handler(uid):
    return select_other(uid)