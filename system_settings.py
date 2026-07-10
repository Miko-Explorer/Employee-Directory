from datetime import datetime
from database import run_query

def get_all_settings():
    return run_query("SELECT * FROM system_settings ORDER BY category, setting_key")

def get_setting(setting_id):
    return run_query("SELECT * FROM system_settings WHERE setting_id = %s", (setting_id,))

def get_setting_by_key(setting_key):
    result = run_query("SELECT * FROM system_settings WHERE setting_key = %s", (setting_key,))
    return result[0] if result else None

def get_settings_by_category(category):
    return run_query(
        "SELECT * FROM system_settings WHERE category = %s ORDER BY setting_key",
        (category,),
    )

def get_categories():
    return run_query("SELECT DISTINCT category FROM system_settings ORDER BY category")

def create_setting(setting_key, setting_value, category, description=None):
    now = datetime.now()
    query = """INSERT INTO system_settings (setting_key, setting_value, category, description, updated_at)
        VALUES (%s, %s, %s, %s, %s)"""
    return run_query(query, (setting_key, setting_value, category, description, now), fetch=False)

def update_setting(setting_id, setting_value=None, description=None):
    fields = []
    params = []
    if setting_value is not None:
        fields.append("setting_value = %s")
        params.append(setting_value)
    if description is not None:
        fields.append("description = %s")
        params.append(description)
    if not fields:
        return 0
    fields.append("updated_at = %s")
    params.append(datetime.now())
    params.append(setting_id)
    query = "UPDATE system_settings SET {} WHERE setting_id = %s".format(", ".join(fields))
    return run_query(query, params, fetch=False)

def delete_setting(setting_id):
    return run_query("DELETE FROM system_settings WHERE setting_id = %s", (setting_id,), fetch=False)

def count_settings():
    result = run_query("SELECT COUNT(*) AS total FROM system_settings")
    return result[0]["total"] if result else 0