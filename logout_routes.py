from flask import Blueprint, jsonify

logout_bp = Blueprint("logout", __name__, url_prefix="/logout")

@logout_bp.route("", methods=["POST"])
def logout():
    try:
        return jsonify({
            "status": "success",
            "message": "Logout berhasil, silakan login kembali jika ingin menggunakan aplikasi."
        }), 200

    except Exception as e:
        print("❌ Error saat logout:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500
