from dal import add_his, select_all



def add_his_handler(uid, type_name, buk, filepath, config, input):
    add_his(uid, type_name, buk, filepath, config, input)

def get_all_his_handler():
    return select_all()