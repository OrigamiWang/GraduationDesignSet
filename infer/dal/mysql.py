from db import MYSQL_CLI

MYSQL_CURSOR = MYSQL_CLI.cursor()

def execute_sql(sql):
    MYSQL_CURSOR.execute(sql)
    return MYSQL_CURSOR.fetchall()