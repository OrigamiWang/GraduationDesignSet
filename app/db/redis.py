import redis

from common import CONFIG

# redis开启远程登陆
# 修改配置文件：
#   1. bind 0.0.0.0
#   2. protected-mode no
#   3. daemonize yes
# 公司搭建环境记得改port！！！

class RedisClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.client = redis.Redis(*args, **kwargs)
        return cls._instance

    def get_client(self):
        return self.client


def connect_redis():
    redis_config = CONFIG['redis']
    return RedisClient(host=redis_config['host'], port=redis_config['port'], password=redis_config['password'])

REDIS_CLI = connect_redis().get_client()

"""
cli = connect_redis()
conn = cli.get_client()
print(conn.get('k'))
"""
