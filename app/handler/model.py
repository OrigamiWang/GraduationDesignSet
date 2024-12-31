from flask import request

from biz import get_model_list, get_lora_by_base_name, get_vae_by_base_name



def get_model_list_handler():
    model_list = get_model_list()
    model_dict_list = [model.to_dict() for model in model_list]
    return model_dict_list

def get_vae_list_by_base_name_handler():
    base_name = request.get_json()['base_name']
    vae_list = get_vae_by_base_name(base_name)
    vae_dict_list = [vae.to_dict() for vae in vae_list]
    return vae_dict_list



def get_lora_list_by_base_name_handler():
    base_name = request.get_json()['base_name']
    lora_list = get_lora_by_base_name(base_name)
    lora_dict_list = [lora.to_dict() for lora in lora_list]

    return lora_dict_list