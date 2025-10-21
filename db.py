import gevent.monkey
gevent.monkey.patch_all()  # <--- INI PENTING!

import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="pg-15053d3a-duri-pintar.j.aivencloud.com",  # ganti sesuai Aiven kamu
        dbname="defaultdb",                     # nama database di Aiven
        user="avnadmin",                         # username dari Aiven
        password="AVNS_eLYY8qHsEq7O8EwibgU",                    # password dari Aiven
        port=20326,                              # port dari Aiven
        sslmode="require"                        # wajib untuk koneksi Aiven
    )

#  HISTORY 
def insert_history(scan_type, result, confidence, filename):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO scan_history (scan_type, result, confidence, filename)
            VALUES (%s, %s, %s, %s)
        """, (scan_type, result, confidence, filename))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("❌ Error insert_history:", e)
        return False

def get_history(limit=10):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)  
        cur.execute("""
            SELECT id, scan_type, result, confidence, filename, timestamp
            FROM scan_history
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ Error get_history:", e)
        return []

#  USERS 
def create_user(nama, email, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (nama, email, password)
            VALUES (%s, %s, %s)
            RETURNING id_user
        """, (nama, email, password))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return user_id
    except Exception as e:
        print("❌ Error create_user:", e)
        return None

def get_user_by_email(email):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        print("❌ Error get_user_by_email:", e)
        return None

def validate_user(email, password):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT id_user, nama, email
            FROM users
            WHERE email = %s AND password = %s
        """, (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        print("❌ Error validate_user:", e)
        return None
