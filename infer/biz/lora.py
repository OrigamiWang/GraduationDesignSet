import torch

from uuid import uuid4
from dal import format_path
from common import LORA

def load_lora(pipe, lora_config):
    adapter_list = []
    weight_list = []
    
    for lora_id, weight in lora_config.items():
        lora_path = format_path(LORA, lora_id)
        rand = str(uuid4()).replace("-", "")
        adapter_name = f'{lora_id.split(".")[0]}_{rand}'
        adapter_list.append(adapter_name)
        weight_list.append(weight)
        pipe.load_lora_weights(lora_path, weight_name=lora_id, adapter_name=adapter_name, torch_dtype=torch.float16)


    pipe.set_adapters(adapter_list, adapter_weights=weight_list)