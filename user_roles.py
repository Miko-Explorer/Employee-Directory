from datetime import datetime
from database import run_query

def get_user_roles(user_id):
    query = """SELECT r.*, ur.assigned_at, ur.assigned_by
        FROM user_roles ur
        JOIN roles r ON ur.role_id = r.role_id
        WHERE ur.user_id = %s
        ORDER BY ur.assigned_at DESC"""
    return run_query(query, (user_id,))

def get_role_users(role_id):
    query = """SELECT u.*, ur.assigned_at, ur.assigned_by
        FROM user_roles ur
        JOIN users u ON ur.user_id = u.user_id
        WHERE ur.role_id = %s AND u.deleted_at IS NULL
        ORDER BY ur.assigned_at DESC"""
    return run_query(query, (role_id,))

def get_all_assignments():
    query = """SELECT u.user_id, u.user_name, u.first_name, u.last_name,
        r.role_id, r.role_name, ur.assigned_at, ur.assigned_by
        FROM user_roles ur
        JOIN users u ON ur.user_id = u.user_id
        JOIN roles r ON ur.role_id = r.role_id
        WHERE u.deleted_at IS NULL
        ORDER BY ur.assigned_at DESC"""
    return run_query(query)

def assign_role(user_id, role_id, assigned_by):
    now = datetime.now()
    query = "INSERT INTO user_roles (user_id, role_id, assigned_at, assigned_by) VALUES (%s, %s, %s, %s)"
    return run_query(query, (user_id, role_id, now, assigned_by), fetch=False)

def remove_role(user_id, role_id):
    query = "DELETE FROM user_roles WHERE user_id = %s AND role_id = %s"
    return run_query(query, (user_id, role_id), fetch=False)

def get_unassigned_users():
    query = """SELECT * FROM users WHERE deleted_at IS NULL
        AND user_id NOT IN (SELECT DISTINCT user_id FROM user_roles)
        ORDER BY user_name"""
    return run_query(query)

def get_available_roles_for_user(user_id):
    query = """SELECT * FROM roles WHERE role_id NOT IN
        (SELECT role_id FROM user_roles WHERE user_id = %s)
        ORDER BY role_name"""
    return run_query(query, (user_id,))

def count_assignments():
    result = run_query("SELECT COUNT(*) AS total FROM user_roles")
    return result[0]["total"] if result else 0