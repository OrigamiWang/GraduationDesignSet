from .mysql import execute_sql
from util import format_filepath
from common import BASE_PATH, LOGGER


def get_base_name(table, name):
    sql = f'SELECT * FROM {table} WHERE name = \'{name}\''
    try:
        res = execute_sql(sql)
    except Exception as e:
        LOGGER.error(f'error: {e}')
    if len(res) == 0:
        return None
    else:
        return res[0][3]
    


def format_path(type_name, name):
    base_name = get_base_name(type_name, name)
    if base_name is None:
        raise Exception("Bad base name or no res in db!")
    res = format_filepath(BASE_PATH, type_name, base_name, name)
    return res