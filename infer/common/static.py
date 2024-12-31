from os import path as osp

from util import read_yaml


common_dir = osp.dirname(osp.abspath(__file__))
CONFIG = read_yaml(osp.join(common_dir, '../','config.yaml'))
ENV = CONFIG['env']


if ENV == "PROD":
    import torch
    DEVICE  = "cuda" if torch.cuda.is_available() else "cpu"
elif ENV == "DEV":
    DEVICE  = "cuda"

PORT = CONFIG['port']
