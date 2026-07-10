from datetime import datetime
from database import run_query

def get_all_permissions():
    return run_query("SELECT * FROM permissions ORDER BY permission_name")

def get_permission_by_id(permission_id):
    return run_query("SELECT * FROM permissions WHERE permission_id = %s", (permission_id,))

def create_permission(permission_name, resource, action, description=None):
    now = datetime.now()
    query = """INSERT INTO permissions (permission_name, resource, action, description, created_at)
        VALUES (%s, %s, %s, %s, %s)"""
    return run_query(query, (permission_name, resource, action, description, now), fetch=False)

def update_permission(permission_id, permission_name=None, resource=None, action=None, description=None):
    fields = []
    params = []
    if permission_name is not None:
        fields.append("permission_name = %s")
        params.append(permission_name)
    if resource is not None:
        fields.append("resource = %s")
        params.append(resource)
    if action is not None:
        fields.append("action = %s")
        params.append(action)
    if description is not None:
        fields.append("description = %s")
        params.append(description)
    if not fields:
        return 0
    params.append(permission_id)
    query = "UPDATE permissions SET {} WHERE permission_id = %s".format(", ".join(fields))
    return run_query(query, params, fetch=False)

def delete_permission(permission_id):
    return run_query("DELETE FROM permissions WHERE permission_id = %s", (permission_id,), fetch=False)

def count_permissions():
    result = run_query("SELECT COUNT(*) AS total FROM permissions")
    return result[0]["total"] if result else 0