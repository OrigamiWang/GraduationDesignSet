from model import Lora
from .mysql import execute_sql


def select_lora_where_base_name(base_name):
    sql = f"SELECT * FROM lora WHERE base_name = \'{base_name}\'"
    res = execute_sql(sql)

    lora_list = []
    for lora_dict in res:
        lora = Lora(lora_dict)
        lora_list.append(lora)

    return lora_list