from flask import Blueprint, jsonify
from db import get_history

history_bp = Blueprint("history", __name__, url_prefix="/history")

@history_bp.route("/", methods=["GET"])
def history():
    try:
        data = get_history(limit=20)

        return jsonify({
            "status": "success",
            "data": data
        }), 200

    except Exception as e:
        print("❌ Error saat ambil history:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500
