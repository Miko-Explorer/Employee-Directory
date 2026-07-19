import streamlit as st
import mysql.connector
from mysql.connector import Error

def get_connection():
    config = st.secrets["mysql"]
    raw_port = config.get("port")
    if raw_port is None or str(raw_port).strip() == "":
        port = 3306
    else:
        try:
            port = int(raw_port)
        except (ValueError, TypeError):
            port = 3306
    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        port=port
    )

def run_query(query, params=None, fetch=True):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def run_many(query, params_list):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.executemany(query, params_list)
        conn.commit()
        return cursor.rowcount
    except Error as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
