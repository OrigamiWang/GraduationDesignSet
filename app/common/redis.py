
from .static import CONFIG



REDIS_KEY = CONFIG['redis']['key']

POD_CNT_KEY = REDIS_KEY['pod_cnt']
SS_NAME_KEY = REDIS_KEY['ss_name']
CACHE_MAP_KEY = REDIS_KEY['cache_map']
EMPTY_QUEUE_KEY = REDIS_KEY['empty_queue']




IMG_EXPIRE_TIME = 24 * 60 * 60 # 一天(单位: s)