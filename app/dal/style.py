from .mysql import execute_sql


def select_all_style():
    sql = "SELECT * FROM sd_style"
    return execute_sql(sql)
