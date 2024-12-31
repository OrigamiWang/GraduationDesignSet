from .config import read_yaml

CONFIG = read_yaml('config.yaml')
ENV = CONFIG['env']


if ENV == "PROD":
    import torch
    DEVICE  = "cuda" if torch.cuda.is_available() else "cpu"
elif ENV == "DEV":
    DEVICE  = "cuda"