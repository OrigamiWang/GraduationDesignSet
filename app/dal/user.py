from .mysql import execute_sql, execute_sql_with_commit


def select_all_users():
    sql = "SELECT * FROM user"
    return execute_sql(sql)

def select_one_user(name):
    sql = f"SELECT * FROM user WHERE `name` = '{name}'"
    return execute_sql(sql)

def insert_user(name, pswd):
    sql = f"INSERT INTO user(`name`, `password`) VALUE('{name}', '{pswd}')"
    execute_sql_with_commit(sql)

def check_user_existance(name, pswd):
    sql = f"SELECT * FROM user WHERE `name`='{name}' and `password`='{pswd}'"
    return execute_sql(sql)