from db import REDIS_CLI


# 设置过期时间(单位: s)
def set_key_expire(key, val, expire_time): 
    REDIS_CLI.set(key, val)
    REDIS_CLI.expire(key, expire_time)

def set_key(key, val): 
    REDIS_CLI.set(key, val)

def get_key(key):
    return REDIS_CLI.get(key)

def flush_expire(key, expire_time):
    REDIS_CLI.expire(key, expire_time)

def get_with_prefix(prefix):
    return REDIS_CLI.scan(cursor='0', match=f'{prefix}*')
    
def zset_add(q, k, s):
    REDIS_CLI.zadd(q, {k: s})
    
def zset_del(q, k):
    REDIS_CLI.zrem(q, k)

# 获取分数最小的
def zset_get_min_score(q):
    return REDIS_CLI.zrange(q, start=0, end=0)

def zset_get_all(q):
    return REDIS_CLI.zrange(q, start=0, end=-1)

def zset_get_with_prefix(q, prefix):
    cursor = '0'
    filtered_members = []
    while cursor != 0:
        cursor, members_with_scores = REDIS_CLI.zscan(q, cursor=cursor, match=prefix)
        filtered_members.extend(members_with_scores)
    return filtered_members

