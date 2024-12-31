import torch
from diffusers import StableDiffusionPipeline


def load_pipeline(model_path):
    print(f'model_path: {model_path}')
    pipe = StableDiffusionPipeline.from_single_file(
        model_path, 
        torch_dtype=torch.float16
    )
    return pipe