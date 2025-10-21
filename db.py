import gevent.monkey
gevent.monkey.patch_all() 

import pymysql.cursors
from pymysql.pool import Pool
from pymysql.converters import escape_string # untuk keamanan

# --- KONFIGURASI CONNECTION POOL (MySQL) ---
DB_NAME = "duri_db"
DB_USER = "durian_user"
DB_PASSWORD = "password1234#" 
DB_HOST = "localhost"
DB_PORT = 3306 # Port default MySQL/MariaDB

# Inisialisasi Connection Pool Global
try:
    conn_pool = Pool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        port=DB_PORT,
        min_size=1, 
        max_size=10, # Sesuaikan
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ MySQL Connection Pool berhasil diinisialisasi.")
except Exception as e:
    print(f"❌ GAGAL membuat MySQL Connection Pool: {e}")
    conn_pool = None 


def get_conn_from_pool():
    """Mengambil koneksi dari pool."""
    if conn_pool is None:
         raise Exception("Connection Pool tidak tersedia.")
    # PyMySQL Pool secara otomatis Thread-safe (dibuat aman oleh Monkey Patch Gevent)
    return conn_pool.get_connection()

def put_conn_to_pool(conn):
    """Mengembalikan koneksi ke pool."""
    if conn_pool is not None and conn is not None:
        conn_pool.close(conn) # Di PyMySQL pool, gunakan close() untuk mengembalikan

# --- FUNGSI DB (Modifikasi sintaks SQL untuk MySQL) ---

#  HISTORY 
def insert_history(scan_type, result, confidence, filename):
    conn = None
    try:
        conn = get_conn_from_pool()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO scan_history (scan_type, result, confidence, filename, timestamp)
            VALUES (%s, %s, %s, %s, NOW())
        """, (scan_type, result, confidence, filename))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print("❌ Error insert_history:", e)
        if conn:
             conn.rollback()
        return False
    finally:
        put_conn_to_pool(conn)


def get_history(limit=10):
    conn = None
    try:
        conn = get_conn_from_pool()
        cur = conn.cursor() 
        # MySQL menggunakan LIMIT tanpa OFFSET
        cur.execute("""
            SELECT id, scan_type, result, confidence, filename, timestamp
            FROM scan_history
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print("❌ Error get_history:", e)
        return []
    finally:
        put_conn_to_pool(conn)


#  USERS 
def create_user(nama, email, password):
    conn = None
    try:
        conn = get_conn_from_pool()
        cur = conn.cursor()
        
        # Cek apakah email sudah ada
        cur.execute("SELECT id_user FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            raise ValueError("Email sudah terdaftar.")

        # Modifikasi INSERT: MySQL menggunakan LAST_INSERT_ID()
        cur.execute(
            "INSERT INTO users (nama, email, password) VALUES (%s, %s, %s)",
            (nama, email, password),
        )
        user_id = cur.lastrowid # Cara mendapatkan ID yang baru dibuat di MySQL
        conn.commit()
        cur.close()
        return user_id
    except ValueError:
        if conn:
             conn.rollback()
        raise 
    except Exception as e:
        print("❌ Error create_user:", e)
        if conn:
             conn.rollback()
        return None
    finally:
        put_conn_to_pool(conn)


def get_user_by_email(email):
    conn = None
    try:
        conn = get_conn_from_pool()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        return user
    except Exception as e:
        print("❌ Error get_user_by_email:", e)
        return None
    finally:
        put_conn_to_pool(conn)


def validate_user(email, password):
    # Logika tetap sama, hanya koneksi yang berubah
    conn = None
    try:
        conn = get_conn_from_pool()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_user, nama, email
            FROM users
            WHERE email = %s AND password = %s
        """, (email, password))
        user = cur.fetchone()
        cur.close()
        return user
    except Exception as e:
        print("❌ Error validate_user:", e)
        return None
    finally:
        put_conn_to_pool(conn)