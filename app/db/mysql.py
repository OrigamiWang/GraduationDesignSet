import pymysql
from common import CONFIG
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

class MysqlClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MysqlClient, cls).__new__(cls)
            # 创建数据库连接池
            cls.pool = PooledDB(
                creator=pymysql,
                maxconnections=10,
                host=CONFIG['mysql']['host'],
                port=CONFIG['mysql']['port'],
                user=CONFIG['mysql']['user'],
                password=CONFIG['mysql']['password'],
                database=CONFIG['mysql']['database'],
                charset='utf8mb4',
                cursorclass=DictCursor
            )
        return cls._instance

    def get_conn(self):
        # 从连接池获取连接
        return self._instance.pool.connection()

def connect_mysql():
    return MysqlClient()

# 使用示例
MYSQL_CLI = connect_mysql()
# MYSQL_CONN = MYSQL_CLI.get_conn()
# MYSQL_CURSOR = MYSQL_CONN.cursor()