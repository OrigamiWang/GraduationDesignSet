from common import DEVICE, CONFIG, CLIP_INTERROGATOR
from util import format_filepath

def generate_prompt(image):
    from clip_interrogator import Config, Interrogator
    
    global CLIP_INTERROGATOR

    
    if CLIP_INTERROGATOR is None:
        print(CONFIG['sd']['prompt_gen']['cache_dir'])
        CLIP_INTERROGATOR = Interrogator(
            Config(
                device=DEVICE,
                clip_model_name=CONFIG['sd']['prompt_gen']['clip_model_name'], 
                cache_path=CONFIG['sd']['prompt_gen']['cache_dir'])
            )
        # CLIP_INTERROGATOR = Interrogator(
        #     Config(
        #         device=DEVICE,
        #         clip_model_name=CONFIG['sd']['prompt_gen']['clip_model_name'], 
        #         cache_path=format_filepath(CONFIG['sd']['prompt_gen']['cache_dir']))
        #     )

            
    return CLIP_INTERROGATOR.interrogate_fast(image)