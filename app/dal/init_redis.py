from .redis import *
import time
from uuid import uuid4

def init_redis():
    pod_cnt = 2
    empty_queue = 'INFER:EMPTY_QUEUE'
    ts = int(time.time())
    
    
    ss_name = 'infer-ss'
    set_key("INFER:POD:CNT", pod_cnt)
    set_key("INFER:POD:SS_NAME", ss_name)
    
    for i in range(pod_cnt):
        uuid = str(uuid4()).replace("-", "")
        zset_add(empty_queue, f"test_model_id:{ss_name}-{i}:{uuid}", ts) # 初始化empty_queue, key设置成随机名字
