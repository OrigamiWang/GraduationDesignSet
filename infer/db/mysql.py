import pymysql
from common import CONFIG


class MysqlClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MysqlClient, cls).__new__(cls)
            cls._instance.client = pymysql.connect(*args, **kwargs)
        return cls._instance

    def get_client(self):
        return self.client


def connect_mysql():
    mysql_config = CONFIG['mysql']
    return MysqlClient(host=mysql_config['host'],
                     port=mysql_config['port'],
                     user=mysql_config['user'],
                     password=mysql_config['password'],
                     database=mysql_config['database'])


MYSQL_CLI = connect_mysql().get_client()

"""
cli = connect_mysql()
conn = cli.get_client()
cursor = conn.cursor()
cursor.execute("SELECT * FROM test")
print(cursor.fetchall())
"""