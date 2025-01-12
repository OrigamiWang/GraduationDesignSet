from .mysql import execute_sql, execute_sql_with_commit
import json

def add_his(uid, type_name, buk, filepath, config={}, input={}):
    config_str = json.dumps(config)
    input_str = json.dumps(input)
    sql = f"INSERT INTO history(`uid`, `type`, `buk`, `path`, `config`, `input`) VALUE({uid}, '{type_name}', '{buk}', '{filepath}', '{config_str}', '{input_str}')"
    execute_sql_with_commit(sql)


def select_all(uid):
    sql = f"SELECT * FROM history WHERE uid={uid} order by id DESC"
    return execute_sql(sql)


def select_other(uid):
    sql = f"SELECT * FROM history WHERE uid!={uid} order by id DESC"
    return execute_sql(sql)
