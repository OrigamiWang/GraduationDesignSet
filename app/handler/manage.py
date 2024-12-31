from biz import get_roles, get_permissions_by_role, get_home_permissions

def get_user_permissions_handler():
    roles = get_roles()
    for role in roles:
        rid = role['id']
        permissions = get_permissions_by_role(rid)
        permit_arr = []
        for permit in permissions:
            permit_arr.append(permit['p_id'])
        role['permissions'] = permit_arr
    return roles

def get_home_permissions_handler():
    begin_id, end_id = 2, 24
    res = get_home_permissions(begin_id, end_id)
    return res