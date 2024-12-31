from common import MODEL, LORA, VAE

"""
用于缓存pipeline、lora、scheduler、vae
"""
class SDCache():

    def __init__(self):
        self.CACHE_MAP = {}
        self.CACHE_MAP[MODEL] = {}
        self.CACHE_MAP[LORA] = {}
        self.CACHE_MAP[VAE] = {}

    
    def cache(self, cache_type, k, v):
        self.CACHE_MAP[cache_type][k] = v

    def read_cache(self, cache_type, k):
        if k in self.CACHE_MAP[cache_type]:
            return self.CACHE_MAP[cache_type][k]
        else:
            return None
    
    """
    flush只是清除某一个类别的缓存
    """
    def flush(self, cache_type):
        self.CACHE_MAP[cache_type] = {}
        
    
    def __str__(self):
        return (
            f"CACHE_MAP: {self.CACHE_MAP}"
        )
    
SD_CACHE = SDCache()