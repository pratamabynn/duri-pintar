from flask import Blueprint, request, jsonify
from db import get_connection
from werkzeug.security import check_password_hash

login_bp = Blueprint('login', __name__, url_prefix="/duri-pintar/login")

@login_bp.route('', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email dan password wajib diisi"
            }), 400

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_user, nama, email, password
            FROM users
            WHERE email = %s
        """, (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[3], password): 
            return jsonify({
                "status": "success",
                "message": "Login berhasil",
                "data": {
                    "id_user": user[0],
                    "nama": user[1],
                    "email": user[2]
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Email atau password salah"
            }), 401

    except Exception as e:
        print("❌ Error saat login:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500
