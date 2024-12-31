import json


taro_json = {
    "negative_prompt": "bad fingers",
    "cfg_scale": 7,
    "steps": 5,
    "model_id": "anything-v4.5.ckpt",
    "lora_config": {
        "AnimeTaroCard.safetensors": 1.0,
        "AtdanLora.safetensors": 0.6
    },
    "sampler_id": "DPM++ 2M Karras",
    "vae_id": "orangemixvaeReupload_v10.pt",
}



d = json.dumps(taro_json,  ensure_ascii=True)
d = d.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
print(d)