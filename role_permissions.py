from datetime import datetime
from database import run_query

def get_role_permissions(role_id):
    query = """SELECT p.*, rp.assigned_at
        FROM role_permissions rp
        JOIN permissions p ON rp.permission_id = p.permission_id
        WHERE rp.role_id = %s
        ORDER BY p.permission_name"""
    return run_query(query, (role_id,))

def get_permission_roles(permission_id):
    query = """SELECT r.*, rp.assigned_at
        FROM role_permissions rp
        JOIN roles r ON rp.role_id = r.role_id
        WHERE rp.permission_id = %s
        ORDER BY r.role_name"""
    return run_query(query, (permission_id,))

def get_all_mappings():
    query = """SELECT r.role_id, r.role_name, p.permission_id, p.permission_name,
        p.resource, p.action, rp.assigned_at
        FROM role_permissions rp
        JOIN roles r ON rp.role_id = r.role_id
        JOIN permissions p ON rp.permission_id = p.permission_id
        ORDER BY r.role_name, p.permission_name"""
    return run_query(query)

def assign_permission(role_id, permission_id):
    now = datetime.now()
    query = "INSERT INTO role_permissions (role_id, permission_id, assigned_at) VALUES (%s, %s, %s)"
    return run_query(query, (role_id, permission_id, now), fetch=False)

def remove_permission(role_id, permission_id):
    query = "DELETE FROM role_permissions WHERE role_id = %s AND permission_id = %s"
    return run_query(query, (role_id, permission_id), fetch=False)

def get_available_permissions_for_role(role_id):
    query = """SELECT * FROM permissions WHERE permission_id NOT IN
        (SELECT permission_id FROM role_permissions WHERE role_id = %s)
        ORDER BY permission_name"""
    return run_query(query, (role_id,))

def get_available_roles_for_permission(permission_id):
    query = """SELECT * FROM roles WHERE role_id NOT IN
        (SELECT role_id FROM role_permissions WHERE permission_id = %s)
        ORDER BY role_name"""
    return run_query(query, (permission_id,))

def count_mappings():
    result = run_query("SELECT COUNT(*) AS total FROM role_permissions")
    return result[0]["total"] if result else 0