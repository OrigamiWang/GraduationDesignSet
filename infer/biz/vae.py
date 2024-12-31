import torch

from diffusers import AutoencoderKL


def load_vae(vae_path):
    return AutoencoderKL.from_single_file(vae_path, torch_dtype=torch.float16)