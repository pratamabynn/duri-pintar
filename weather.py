from flask import Blueprint, request, jsonify
import requests

weather_bp = Blueprint("weather", __name__, url_prefix="/duri-pintar/weather")

OPENWEATHER_API_KEY = "de357b9909f8fd8ae8515a879d689a38"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@weather_bp.route('', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"status": "error", "message": "Parameter city wajib diisi"}), 400

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(OPENWEATHER_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data cuaca",
                "details": data
            }), response.status_code

        result = {
            "status": "success",
            "data": {
                "city": data.get("name"),
                "temperature": data["main"]["temp"],
                "weather": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
        }
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500
