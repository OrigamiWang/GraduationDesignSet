import json
from flask import request
import copy
import time

from biz import get_and_cache_img_prompt, wait_for_pod_name
from model import SDMetaData, TxtPromptData, ImgPromptData, ImgData, InferData, ExtData, ModelData, LoraConfig
from util import get_map_val, forward, MINIO_CLI
from common import LOGGER, CONFIG
from dal import add_his

def generate_handler():
    req_dict = request.get_json()
    
    uid = get_map_val(req_dict, 'uid')
    type_name = get_map_val(req_dict, 'type')
    copy_req_dict = copy.deepcopy(req_dict)

    keys_to_del = ['uid', 'type', 'img_base64_str']
    for key in keys_to_del:
        if key in copy_req_dict:
            del copy_req_dict[key]

    img_data = ImgData(get_map_val(req_dict, 'width'), 
                       get_map_val(req_dict, 'height'))
    infer_data = InferData(get_map_val(req_dict, 'cfg_scale'), 
                           get_map_val(req_dict, 'seed'),
                           get_map_val(req_dict, 'steps'))
    ext_data = ExtData(get_map_val(req_dict, 'batch_size'), 
                       get_map_val(req_dict, 'batch_cnt'))
    lora_config = LoraConfig(get_map_val(req_dict, 'lora_config'))
    model_data = ModelData(get_map_val(req_dict, 'model_id'), 
                           lora_config, 
                           get_map_val(req_dict, 'sampler_id'), 
                           get_map_val(req_dict, 'vae_id'))
    
    b64_img_list = []

    if req_dict['txt2img']:
        # txt2img
        print("===txt2img===")
        prompt_data = TxtPromptData(get_map_val(req_dict, 'prompt'), 
                                    get_map_val(req_dict, 'negative_prompt'))

        sd_meta_data = SDMetaData(img_data, model_data, prompt_data, infer_data, ext_data)
        model_id = sd_meta_data.model_data.model_id
        pod_name = wait_for_pod_name(model_id)
        proxy_url_template = CONFIG['proxy']['infer']['url_template']

        proxy_url = proxy_url_template.format(pod_name)
        proxy_url = "http://127.0.0.1:4000/infer/txt2img"
        # FIX_ME: 这里暂时用的虚假的url，先完善infer
        req_body = sd_meta_data.to_dict()
        resp = forward(method='post', url=proxy_url, data=req_body)
        LOGGER.info(f'proxy_url: {proxy_url}')
        LOGGER.info(f'pod_name: {pod_name}')
        # byte to str
        b64_img_list = json.loads(resp.content)
    else:
        # img2img
        print("===img2img===")
        extra_prompt = get_and_cache_img_prompt(get_map_val(req_dict, 'img_base64_str'))
        print(f"extra_prompt: {extra_prompt}")
        prompt_data = ImgPromptData(extra_prompt, get_map_val(req_dict, 'negative_prompt'))
        
        sd_meta_data = SDMetaData(img_data, model_data, prompt_data, infer_data, ext_data)
        # print(sd_meta_data)
        model_id = sd_meta_data.model_data.model_id
        pod_name = wait_for_pod_name(model_id)
        proxy_url_template = CONFIG['proxy']['infer']['url_template']

        proxy_url = proxy_url_template.format(pod_name)
        # FIX_ME: 这里暂时用的虚假的url，先完善infer
        req_body = sd_meta_data.to_dict()
        resp = forward(method='post', url=proxy_url, data=req_body)
        LOGGER.info(f'proxy_url: {proxy_url}')
        LOGGER.info(f'pod_name: {pod_name}')
        # byte to str
        b64_img_list = json.loads(resp.content)
    url_list = []
    file_list = []
    for idx in range(len(b64_img_list)):
        b64_img = b64_img_list[idx]
        filename = f'{str(time.time()).replace(".", "")}{idx}'
        filepath = f"user-{uid}/{type_name}/{filename}.png"
        file_list.append(filepath)
        # 上传图片到oss并返回在线url结果
        presigned_url = MINIO_CLI.upload_file("stable-diffusion", filepath, b64_img)
        url_list.append(presigned_url)
    for filepath in file_list:
        add_his(uid, type_name, "stable-diffusion", filepath, config=copy_req_dict, input={})
    # 将结果也保存一份到mysql作为历史记录
    
    return json.dumps(url_list)


def avatar_handler():
    req_dict = request.get_json()
    
    
    img_data = ImgData(get_map_val(req_dict, 'width'), 
                       get_map_val(req_dict, 'height'))
    infer_data = InferData(get_map_val(req_dict, 'cfg_scale'), 
                           get_map_val(req_dict, 'seed'),
                           get_map_val(req_dict, 'steps'))
    ext_data = ExtData(get_map_val(req_dict, 'batch_size'), 
                       get_map_val(req_dict, 'batch_cnt'))
    lora_config = LoraConfig(get_map_val(req_dict, 'lora_config'))
    model_data = ModelData(get_map_val(req_dict, 'model_id'), 
                           lora_config, 
                           get_map_val(req_dict, 'sampler_id'), 
                           get_map_val(req_dict, 'vae_id'))
    
    
    print("===avatar===")
    extra_prompt = get_and_cache_img_prompt(get_map_val(req_dict, 'img_base64_str'))
    print(f"extra_prompt: {extra_prompt}")
    prompt_data = ImgPromptData(extra_prompt, get_map_val(req_dict, 'negative_prompt'))
    
    sd_meta_data = SDMetaData(img_data, model_data, prompt_data, infer_data, ext_data)
    # print(sd_meta_data)
    model_id = sd_meta_data.model_data.model_id
    pod_name = wait_for_pod_name(model_id)
    proxy_url_template = CONFIG['proxy']['infer']['url_template']

    proxy_url = proxy_url_template.format(pod_name)
    proxy_url = "http://127.0.0.1:4000/infer/gen_avatar"
    # FIX_ME: 这里暂时用的虚假的url，先完善infer
    req_body = sd_meta_data.to_dict()
    resp = forward(method='post', url=proxy_url, data=req_body)
    LOGGER.info(f'proxy_url: {proxy_url}')
    LOGGER.info(f'pod_name: {pod_name}')
    # byte to str
    return json.dumps(json.loads(resp.content))
