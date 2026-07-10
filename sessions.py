import secrets
from datetime import datetime, timedelta
from database import run_query

def create_session(user_id, ip_address, user_agent, expires_in_minutes=60):
    session_token = secrets.token_hex(32)
    now = datetime.now()
    expires_at = now + timedelta(minutes=expires_in_minutes)
    query = """INSERT INTO sessions (user_id, session_token, ip_address, user_agent, expires_at, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)"""
    return run_query(
        query, (user_id, session_token, ip_address, user_agent, expires_at, now),
        fetch=False,
    )

def get_session_by_token(token):
    return run_query("SELECT * FROM sessions WHERE session_token = %s", (token,))

def get_user_sessions(user_id):
    return run_query(
        "SELECT * FROM sessions WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )

def get_all_sessions():
    return run_query(
        """SELECT s.*, u.user_name, u.first_name, u.last_name
        FROM sessions s JOIN users u ON s.user_id = u.user_id
        ORDER BY s.created_at DESC"""
    )

def get_active_sessions():
    return run_query(
        """SELECT s.*, u.user_name, u.first_name, u.last_name
        FROM sessions s JOIN users u ON s.user_id = u.user_id
        WHERE s.expires_at > NOW()
        ORDER BY s.created_at DESC"""
    )

def expire_session(session_id):
    now = datetime.now()
    query = "UPDATE sessions SET expires_at = %s WHERE session_id = %s"
    return run_query(query, (now, session_id), fetch=False)

def delete_expired_sessions():
    query = "DELETE FROM sessions WHERE expires_at <= NOW()"
    return run_query(query, fetch=False)

def count_sessions():
    result = run_query("SELECT COUNT(*) AS total FROM sessions")
    return result[0]["total"] if result else 0

def count_active_sessions():
    result = run_query("SELECT COUNT(*) AS total FROM sessions WHERE expires_at > NOW()")
    return result[0]["total"] if result else 0