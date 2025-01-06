import torch

from .cache import SD_CACHE
from .pipeline import load_pipeline
from .sampler import SAMPLER
from .vae import load_vae
from .lora import load_lora
from common import MODEL, VAE, DEVICE
from dal import format_path
from util import encode_base64



def _has_cache(type_id, type_model_id):
    cache = SD_CACHE.read_cache(type_id, type_model_id)
    has_cache = cache is not None
    return cache, has_cache

def txt2img(model_id, sampler_id, vae_id=None, lora_config=None, width=720, height=1280,
            prompt='', negative_prompt='', cfg_scale=7, steps=50, batch_size=1, batch_cnt=5, seed=-1):

    model_path = format_path(MODEL, model_id)
    
    # base model
    pipe, has_cache = _has_cache(MODEL, model_id)
    if not has_cache:
        SD_CACHE.flush(MODEL)
        pipe = load_pipeline(model_path)
        
        SD_CACHE.cache(MODEL, model_id, pipe)

    # sampler
    sampler = SAMPLER(pipe)
    scheduler = sampler.load(sampler_id)

    if scheduler is None:
        raise Exception("bad sampler id")
    pipe.scheduler = scheduler

    # vae
    if vae_id is not None:
        vae_path = format_path(VAE, vae_id)
        pipe.vae = load_vae(vae_path) 
        
    # lora
    if lora_config is not None:
        load_lora(pipe, lora_config)
    
    # moving pipe to GPU
    pipe = pipe.to(DEVICE)

    # gen img
    images = {}
    raw_seed = seed
    for idx in range(batch_cnt):
        if raw_seed == -1:
            seed = torch.randint(0, 2**32 - 1, (1,)).item()
        image = pipe(
                    height=height,
                    width=width,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=steps,
                    guidance_scale=cfg_scale,
                    generator=torch.manual_seed(seed)).images[0]
        images[idx] = image
    
    output_imgs = []
    for seed, image in images.items():
        output_img = f"temp_output/generated_image_{seed}.png"
        image.save(output_img)
        output_imgs.append(encode_base64(output_img))
        # FIXME: 这里可以优化成保存文件到COS，然后返回COS的URL
    return output_imgs


