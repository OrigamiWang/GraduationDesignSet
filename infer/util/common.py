
def get_with_default(target, default):
    if target is None:
        return default
    else:
        return target
    
def get_json_val(json, k):
    if json is None:
        return None
    if k in json:
        return json[k]
    else:
        return None