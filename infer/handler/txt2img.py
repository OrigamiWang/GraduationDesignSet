from biz import txt2img
from util import get_json_val

def txt2img_handler(j):
    img_data = get_json_val(j, 'img_data')
    width = get_json_val(img_data, 'width')
    height = get_json_val(img_data, 'height')

    model_data = get_json_val(j, 'model_data')
    model_id = get_json_val(model_data, 'model_id')
    lora_config = get_json_val(model_data, 'lora_config')
    sampler_id = get_json_val(model_data, 'sampler_id')
    vae_id = get_json_val(model_data, 'vae_id')

    prompt_data = get_json_val(j, 'prompt_data')
    prompt = get_json_val(prompt_data, 'prompt')
    negative_prompt = get_json_val(prompt_data, 'negative_prompt')

    infer_data = get_json_val(j, 'infer_data')
    cfg_scale = get_json_val(infer_data, 'cfg_scale')
    steps = get_json_val(infer_data, 'steps')
    seed = get_json_val(infer_data, 'seed')

    ext_data = get_json_val(j, 'ext_data')
    batch_size = get_json_val(ext_data, 'batch_size')
    batch_cnt = get_json_val(ext_data, 'batch_cnt')

    return txt2img(model_id, sampler_id, vae_id, lora_config, width, height,
            prompt, negative_prompt, cfg_scale, steps, batch_size, batch_cnt, seed)