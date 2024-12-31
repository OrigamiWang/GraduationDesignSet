from common import IMG_EXPIRE_TIME
from .prompt import generate_prompt
from util import b64_to_img, md5
from dal import get_key, set_key_expire, flush_expire


"""
由于同一张图片的推理结果固定，则可以查redis缓存，复用推理结果
由于同一张图片的复用率不高，那么可以并设置过期时间
"""
def get_and_cache_img_prompt(img_base64):
    
    md5_key = md5(img_base64)
    
    redis_key = f'SD:IMG:{md5_key}'

    extra_prompt = get_key(redis_key)
    
    if not extra_prompt:
        # 没有缓存
        print("===没有缓存===")
        img = b64_to_img(img_base64)
        extra_prompt = generate_prompt(img)
        set_key_expire(redis_key, extra_prompt, IMG_EXPIRE_TIME)
    else:
        # 有缓存
        print("===有缓存===")
        flush_expire(redis_key, IMG_EXPIRE_TIME)
        
    return extra_prompt