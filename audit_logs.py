from datetime import datetime
from database import run_query

def log_action(user_id, action, table_name=None, record_id=None, old_values=None, new_values=None, ip_address="", user_agent=""):
    now = datetime.now()
    query = """INSERT INTO audit_logs
        (user_id, action, table_name, record_id, old_values, new_values, ip_address, user_agent, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    return run_query(
        query,
        (user_id, action, table_name, record_id, old_values, new_values, ip_address, user_agent, now),
        fetch=False,
    )

def get_all_logs(limit=200):
    return run_query(
        """SELECT al.*, u.user_name, u.first_name, u.last_name
        FROM audit_logs al LEFT JOIN users u ON al.user_id = u.user_id
        ORDER BY al.created_at DESC LIMIT %s""",
        (limit,),
    )

def get_user_audit_logs(user_id, limit=100):
    return run_query(
        """SELECT al.*, u.user_name, u.first_name, u.last_name
        FROM audit_logs al LEFT JOIN users u ON al.user_id = u.user_id
        WHERE al.user_id = %s
        ORDER BY al.created_at DESC LIMIT %s""",
        (user_id, limit),
    )

def get_logs_by_action(action, limit=100):
    return run_query(
        """SELECT al.*, u.user_name, u.first_name, u.last_name
        FROM audit_logs al LEFT JOIN users u ON al.user_id = u.user_id
        WHERE al.action = %s
        ORDER BY al.created_at DESC LIMIT %s""",
        (action, limit),
    )

def get_logs_by_table(table_name, limit=100):
    return run_query(
        """SELECT al.*, u.user_name, u.first_name, u.last_name
        FROM audit_logs al LEFT JOIN users u ON al.user_id = u.user_id
        WHERE al.table_name = %s
        ORDER BY al.created_at DESC LIMIT %s""",
        (table_name, limit),
    )

def get_logs_by_date_range(start_date, end_date, limit=200):
    query = """SELECT al.*, u.user_name, u.first_name, u.last_name
        FROM audit_logs al LEFT JOIN users u ON al.user_id = u.user_id
        WHERE al.created_at BETWEEN %s AND %s
        ORDER BY al.created_at DESC LIMIT %s"""
    return run_query(query, (start_date, end_date, limit))

def count_logs():
    result = run_query("SELECT COUNT(*) AS total FROM audit_logs")
    return result[0]["total"] if result else 0

def count_logs_today():
    today = datetime.now().strftime("%Y-%m-%d")
    result = run_query(
        "SELECT COUNT(*) AS total FROM audit_logs WHERE DATE(created_at) = %s",
        (today,),
    )
    return result[0]["total"] if result else 0