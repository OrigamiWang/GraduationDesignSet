

"""
如果key不存在返回None
"""
def get_map_val(map, key):
    if key in map:
        return map[key]
    return None