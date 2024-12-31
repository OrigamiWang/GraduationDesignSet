from abc import ABCMeta, abstractmethod

from common import CONFIG



class ImgData():
    def __init__(self, width, height):
        self.width = width
        self.height = height

class ModelData():
    def __init__(self, model_id, lora_config=None, sampler_id=None, vae_id=None):
        self.model_id = model_id
        self.lora_config = lora_config
        self.sampler_id = sampler_id
        self.vae_id = vae_id
    def __str__(self):
        return ("{\n"
                f"\t\tmodel_id: {self.model_id}\n"
                f"\t\tlora_config: {self.lora_config.__str__()}\n"
                f"\t\tsampler_id: {self.sampler_id}\n"
                f"\t\tvae_id: {self.vae_id}\n"
                "\t}"
        )

    def to_dict(self):
        return {'model_id': self.model_id, 
                'lora_config': self.lora_config.to_dict(), 
                'sampler_id': self.sampler_id,
                'vae_id': self.vae_id}



class LoraConfig():
    def __init__(self, lora_config):
        self.lora_config = lora_config
    def __str__(self):
        return f'lora_config: {self.lora_config}'
    def to_dict(self):
        return self.lora_config  

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
        self.prompt = ''
        self.negative_prompt = ''

    @abstractmethod
    def _preprocess_data(self):
        pass

    def _concat_prompt(self):
        self.prompt = f'{self.base_prompt},{self.extra_prompt}'
        self.negative_prompt = f'{self.base_negative_prompt},{self.extra_negative_prompt}'
        
    def __str__(self):
        return ("{\n"
                f"\t\tprompt: {self.prompt}\n" 
                f"\t\tnegative_prompt: {self.negative_prompt}\n"
                "\t}\n")
    
    def to_dict(self):
        return {'prompt': self.prompt, 'negative_prompt': self.negative_prompt}

class TxtPromptData(PromptData):
    def __init__(self, extra_prompt='', extra_negative_prompt=''):
        super().__init__() 
        self.extra_prompt = extra_prompt
        self.extra_negative_prompt = extra_negative_prompt
        self._preprocess_data()

    
    def _preprocess_data(self):
        self._concat_prompt()


class ImgPromptData(PromptData):
    def __init__(self, extra_prompt='', extra_negative_prompt=''):
        super().__init__() 
        self.prompt = ''
        self.extra_prompt=extra_prompt
        self.extra_negative_prompt = extra_negative_prompt
        self._preprocess_data()
    
    
    def _preprocess_data(self):
        self._concat_prompt()

        
        
class SDMetaData():
    def __init__(self, 
                 img_data: ImgData, 
                 model_data: ModelData, 
                 prompt_data: PromptData,
                 infer_data: InferData,
                 ext_data: ExtData):
        
        self.img_data = img_data
        self.model_data = model_data
        self.prompt_data = prompt_data
        self.infer_data = infer_data
        self.ext_data = ext_data
        
    
    def __str__(self):
        return (f"\nSDMetaData: \n"
                "{"
                f"\timg_data: {self.img_data.__dict__}\n"
                f"\tmodel_data: {self.model_data.__str__()}\n"
                f"\tprompt_data: {self.prompt_data.__str__()}\n"
                f"\tinfer_data: {self.infer_data.__dict__}\n"
                f"\text_data: {self.ext_data.__dict__}\n"
                "}\n")

    def to_dict(self):
        """将SDMetaData对象转换为字典"""
        return {
            'img_data': self.img_data.__dict__,
            'model_data': self.model_data.to_dict(),
            'prompt_data': self.prompt_data.to_dict(),
            'infer_data': self.infer_data.__dict__,
            'ext_data': self.ext_data.__dict__
        }
    