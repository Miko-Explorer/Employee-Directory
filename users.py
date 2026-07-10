import hashlib
import os
from datetime import datetime
from database import run_query, run_many

def _hash_password(password):
    salt = os.urandom(32).hex()
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash, salt

def get_all_users(include_deleted=False):
    query = "SELECT * FROM users"
    if not include_deleted:
        query += " WHERE deleted_at IS NULL"
    query += " ORDER BY created_at DESC"
    return run_query(query)

def get_user_by_id(user_id):
    return run_query("SELECT * FROM users WHERE user_id = %s", (user_id,))

def get_user_by_username(username):
    return run_query("SELECT * FROM users WHERE user_name = %s", (username,))

def get_user_by_email(email):
    return run_query("SELECT * FROM users WHERE email = %s", (email,))

def create_user(user_name, email, password, first_name, last_name, phone_number, profile_picture_url="", status="active"):
    password_hash, salt = _hash_password(password)
    now = datetime.now()
    query = """INSERT INTO users
        (user_name, email, password_hash, salt, first_name, last_name,
         phone_number, profile_picture_url, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    params = (user_name, email, password_hash, salt, first_name, last_name,
              phone_number, profile_picture_url, status, now, now)
    return run_query(query, params, fetch=False)

def update_user(user_id, first_name=None, last_name=None, email=None, phone_number=None, profile_picture_url=None, status=None):
    fields = []
    params = []
    if first_name is not None:
        fields.append("first_name = %s")
        params.append(first_name)
    if last_name is not None:
        fields.append("last_name = %s")
        params.append(last_name)
    if email is not None:
        fields.append("email = %s")
        params.append(email)
    if phone_number is not None:
        fields.append("phone_number = %s")
        params.append(phone_number)
    if profile_picture_url is not None:
        fields.append("profile_picture_url = %s")
        params.append(profile_picture_url)
    if status is not None:
        fields.append("status = %s")
        params.append(status)
    if not fields:
        return 0
    fields.append("updated_at = %s")
    params.append(datetime.now())
    params.append(user_id)
    query = "UPDATE users SET {} WHERE user_id = %s".format(", ".join(fields))
    return run_query(query, params, fetch=False)

def soft_delete_user(user_id):
    now = datetime.now()
    query = "UPDATE users SET deleted_at = %s, updated_at = %s WHERE user_id = %s AND deleted_at IS NULL"
    return run_query(query, (now, now, user_id), fetch=False)

def restore_user(user_id):
    now = datetime.now()
    query = "UPDATE users SET deleted_at = NULL, updated_at = %s WHERE user_id = %s"
    return run_query(query, (now, user_id), fetch=False)

def search_users(term):
    pattern = f"%{term}%"
    query = """SELECT * FROM users WHERE deleted_at IS NULL AND
        (user_name LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s)
        ORDER BY created_at DESC"""
    return run_query(query, (pattern, pattern, pattern, pattern))

def filter_by_status(status):
    query = "SELECT * FROM users WHERE deleted_at IS NULL AND status = %s ORDER BY created_at DESC"
    return run_query(query, (status,))

def update_last_login(user_id, ip_address):
    now = datetime.now()
    query = "UPDATE users SET last_login_ip = %s, last_login_at = %s WHERE user_id = %s"
    return run_query(query, (ip_address, now, user_id), fetch=False)

def count_users():
    result = run_query("SELECT COUNT(*) AS total FROM users WHERE deleted_at IS NULL")
    return result[0]["total"] if result else 0

def count_by_status():
    return run_query("SELECT status, COUNT(*) AS count FROM users WHERE deleted_at IS NULL GROUP BY status")