from db import MYSQL_CLI




def execute_sql(sql):
    MYSQL_CONN = MYSQL_CLI.get_conn()
    with MYSQL_CONN.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result