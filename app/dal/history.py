from .mysql import execute_sql, execute_sql_with_commit
import json

def add_his(uid, type_name, buk, filepath, config={}, input={}):
    config_str = json.dumps(config)
    input_str = json.dumps(input)
    sql = f"INSERT INTO history(`uid`, `type`, `buk`, `path`, `config`, `input`) VALUE({uid}, '{type_name}', '{buk}', '{filepath}', '{config_str}', '{input_str}')"
    execute_sql_with_commit(sql)


def select_all():
    sql = "SELECT * FROM history order by id DESC"
    return execute_sql(sql)
