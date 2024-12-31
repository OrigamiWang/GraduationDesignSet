from dal import select_all_roles, select_all_permissions_by_role, select_permissions_by_id_scale

def get_roles():
    return select_all_roles()

def get_permissions_by_role(rid):
    return select_all_permissions_by_role(rid)

def get_home_permissions(begin_id, end_id):
    return select_permissions_by_id_scale(begin_id, end_id)