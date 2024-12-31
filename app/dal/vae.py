from model import Vae
from .mysql import execute_sql

def select_vae_where_base_name(base_name):
    sql = f"SELECT * FROM vae WHERE base_name = \'{base_name}\'"
    res = execute_sql(sql)
    
    vae_list = []
    for vae_dict in res:
        vae = Vae(vae_dict)
        vae_list.append(vae)

    return vae_list
