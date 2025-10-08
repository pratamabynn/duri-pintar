# register.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from db import get_connection

register_bp = Blueprint("register", __name__) 

@register_bp.route("/duri-pintar/register", methods=["POST"])
def register():
    data = request.get_json()
    nama = data.get("nama")
    email = data.get("email")
    password = data.get("password")

    if not nama or not email or not password:
        return jsonify({"status": "error", "message": "Semua field wajib diisi"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_user FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"status": "error", "message": "Email sudah terdaftar"}), 400

        cur.execute(
            "INSERT INTO users (nama, email, password) VALUES (%s, %s, %s) RETURNING id_user",
            (nama, email, hashed_password),
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "User berhasil didaftarkan",
            "data": {"id_user": user_id, "nama": nama, "email": email}
        }), 201
        
    except Exception as e:
        print("❌ Error register:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
