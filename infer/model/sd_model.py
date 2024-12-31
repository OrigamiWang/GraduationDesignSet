from abc import ABCMeta, abstractmethod

from common import CONFIG
from handler import generate_prompt
from util import b64_to_img


class SDMetaData():
    def __init__(self):
        pass
     

class ImgData():
    def __init__(self, width, height):
        self.width = width
        self.height = height

class ModelData():
    def __init__(self, model_id, lora_id, vae_id, sampler_id):
        self.model_id = model_id
        self.lora_id = lora_id
        self.vae_id = vae_id
        self.sampler_id = sampler_id

class InferData():
    def __init__(self, cfg_scale, seed, steps):
        self.cfg_scale = cfg_scale
        self.seed = seed
        self.steps = steps

class ExtData():
    def __init__(self, batch_size, batch_cnt):
        self.batch_size = batch_size
        self.batch_cnt = batch_cnt


class PromptData(metaclass=ABCMeta):
    def __init__(self):
        self.base_prompt = CONFIG['sd']['meta_data']['prompt']
        self.base_negative_prompt = CONFIG['sd']['meta_data']['negative_prompt']
        self.extra_prompt = ''
        self.extra_negative_prompt = ''
        
    @abstractmethod
    def _preprocess_data(self):
        pass

    def _concat_prompt(self):
        self.prompt = f'{self.base_prompt},{self.extra_prompt}'
        self.negative_prompt = f'{self.base_negative_prompt},{self.extra_negative_prompt}'
        
    def __str__(self):
        return f'prompt: {self.prompt}, negative_prompt: {self.negative_prompt}'
    
    

class TxtPromptData(PromptData):
    def __init__(self, extra_prompt='', extra_negative_prompt=''):
        super().__init__() 
        self.extra_prompt = extra_prompt
        self.extra_negative_prompt = extra_negative_prompt
        self._preprocess_data()

    
    def _preprocess_data(self):
        self._concat_prompt()


class ImgPromptData(PromptData):
    def __init__(self, img_base64, extra_negative_prompt=''):
        super().__init__() 
        self.prompt = ''
        self.img_base64 = img_base64
        self.extra_negative_prompt = extra_negative_prompt
        self._preprocess_data()
    
    
    def _preprocess_data(self):
        img = b64_to_img(self.img_base64)
        
        self.extra_prompt = generate_prompt(img)
        self._concat_prompt()
        