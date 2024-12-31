from dal import *

def get_model_list():
    return select_all_model()

def get_vae_by_base_name(base_name):
    return select_vae_where_base_name(base_name)


def get_lora_by_base_name(base_name):
    return select_lora_where_base_name(base_name)