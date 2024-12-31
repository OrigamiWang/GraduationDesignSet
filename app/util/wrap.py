from functools import wraps
import time
from uuid import uuid4


def standard_response(func):
    def wrap_res(func_res):
        ts = int(time.time())
        requestId = str(uuid4()).replace("-", "")
        res = {
            "ts": ts,
            "requestId": requestId,
            "result": func_res
        }
        return res

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_res = func(*args, **kwargs)
        return wrap_res(func_res)
    return wrapper



