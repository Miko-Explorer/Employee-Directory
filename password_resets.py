import secrets
from datetime import datetime, timedelta
from database import run_query

def create_reset_token(user_id, expires_in_minutes=60):
    token = secrets.token_urlsafe(48)
    now = datetime.now()
    expires_at = now + timedelta(minutes=expires_in_minutes)
    query = """INSERT INTO password_resets (user_id, token, expires_at, created_at)
        VALUES (%s, %s, %s, %s)"""
    return run_query(query, (user_id, token, expires_at, now), fetch=False)

def get_reset_by_token(token):
    return run_query("SELECT * FROM password_resets WHERE token = %s", (token,))

def get_user_resets(user_id):
    return run_query(
        "SELECT * FROM password_resets WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )

def get_all_resets():
    return run_query(
        """SELECT pr.*, u.user_name, u.first_name, u.last_name
        FROM password_resets pr JOIN users u ON pr.user_id = u.user_id
        ORDER BY pr.created_at DESC"""
    )

def mark_token_used(reset_id):
    now = datetime.now()
    query = "UPDATE password_resets SET used_at = %s WHERE reset_id = %s"
    return run_query(query, (now, reset_id), fetch=False)

def is_token_valid(token):
    result = get_reset_by_token(token)
    if not result:
        return False
    r = result[0]
    if r["used_at"] is not None:
        return False
    if r["expires_at"] < datetime.now():
        return False
    return True

def count_resets():
    result = run_query("SELECT COUNT(*) AS total FROM password_resets")
    return result[0]["total"] if result else 0

def count_pending_resets():
    result = run_query(
        "SELECT COUNT(*) AS total FROM password_resets WHERE used_at IS NULL AND expires_at > NOW()"
    )
    return result[0]["total"] if result else 0