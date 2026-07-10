import secrets
from datetime import datetime, timedelta
from database import run_query

def create_verification(user_id, expires_in_minutes=1440):
    token = secrets.token_urlsafe(48)
    now = datetime.now()
    expires_at = now + timedelta(minutes=expires_in_minutes)
    query = """INSERT INTO email_verifications (user_id, token, expires_at, created_at)
        VALUES (%s, %s, %s, %s)"""
    return run_query(query, (user_id, token, expires_at, now), fetch=False)

def get_verification_by_token(token):
    return run_query("SELECT * FROM email_verifications WHERE token = %s", (token,))

def get_user_verifications(user_id):
    return run_query(
        "SELECT * FROM email_verifications WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )

def get_all_verifications():
    return run_query(
        """SELECT ev.*, u.user_name, u.first_name, u.last_name
        FROM email_verifications ev JOIN users u ON ev.user_id = u.user_id
        ORDER BY ev.created_at DESC"""
    )

def verify_email(verification_id):
    now = datetime.now()
    query = "UPDATE email_verifications SET verified_at = %s WHERE verification_id = %s"
    return run_query(query, (now, verification_id), fetch=False)

def is_token_valid(token):
    result = get_verification_by_token(token)
    if not result:
        return False
    r = result[0]
    if r["verified_at"] is not None:
        return False
    if r["expires_at"] < datetime.now():
        return False
    return True

def count_verifications():
    result = run_query("SELECT COUNT(*) AS total FROM email_verifications")
    return result[0]["total"] if result else 0

def count_verified():
    result = run_query(
        "SELECT COUNT(*) AS total FROM email_verifications WHERE verified_at IS NOT NULL"
    )
    return result[0]["total"] if result else 0