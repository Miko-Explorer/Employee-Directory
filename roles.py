from datetime import datetime
from database import run_query

def get_all_roles():
    return run_query("SELECT * FROM roles ORDER BY role_name")

def get_role_by_id(role_id):
    return run_query("SELECT * FROM roles WHERE role_id = %s", (role_id,))

def create_role(role_name, description=None):
    now = datetime.now()
    query = "INSERT INTO roles (role_name, description, created_at, updated_at) VALUES (%s, %s, %s, %s)"
    return run_query(query, (role_name, description, now, now), fetch=False)

def update_role(role_id, role_name=None, description=None):
    fields = []
    params = []
    if role_name is not None:
        fields.append("role_name = %s")
        params.append(role_name)
    if description is not None:
        fields.append("description = %s")
        params.append(description)
    if not fields:
        return 0
    fields.append("updated_at = %s")
    params.append(datetime.now())
    params.append(role_id)
    query = "UPDATE roles SET {} WHERE role_id = %s".format(", ".join(fields))
    return run_query(query, params, fetch=False)

def delete_role(role_id):
    return run_query("DELETE FROM roles WHERE role_id = %s", (role_id,), fetch=False)

def count_roles():
    result = run_query("SELECT COUNT(*) AS total FROM roles")
    return result[0]["total"] if result else 0