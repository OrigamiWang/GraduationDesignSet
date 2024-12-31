from model import Model
from .mysql import execute_sql

def select_all_model():
    sql = "SELECT * FROM model"
    res = execute_sql(sql)
    
    model_list = []
    for model_dict in res:
        model = Model(model_dict)
        model_list.append(model)

    return model_list


