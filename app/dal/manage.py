from .mysql import execute_sql


def select_all_roles():
    sql = "SELECT * FROM role"
    return execute_sql(sql)

def select_all_permissions_by_role(role_id):
    sql = f'SELECT * FROM role_permission WHERE r_id = {role_id}' 
    return execute_sql(sql)


def select_permissions_by_id_scale(begin_id, end_id):
    sql = f'SELECT * FROM permission WHERE id >= {begin_id} AND id <= {end_id}'
    return execute_sql(sql)