from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
import numpy as np
from io import BytesIO
from db import insert_history

jenis_bp = Blueprint('jenis', __name__, url_prefix="/duri-pintar/jenis")

print("🔄 Loading model jenis durian...")
model_jenis = load_model("jenis-durian.h5")
print("✅ Model jenis durian berhasil dimuat.")

labels_jenis = [
    "BENGKULU DURIAN",
    "D24(SULTAN) DURIAN",
    "GOLDENPHOENIX DURIAN",
    "KOTA AGUNG DURIAN",
    "MEDAN DURIAN",
    "MUSANG KING DURIAN",
    "SUMATRA SUPER DURIAN"
]

# Fungsi preprocess sesuai Xception
def preprocess_image(img_bytes):
    img = image.load_img(BytesIO(img_bytes), target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

@jenis_bp.route('/predict-jenis', methods=['POST'])
def predict_jenis():
    try:
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "Tidak ada file yang diupload, gunakan key 'file'"
            }), 400

        file = request.files['file']
        print(f"📂 File diterima untuk deteksi jenis: {file.filename}")

        img_array = preprocess_image(file.read())

        predictions = model_jenis.predict(img_array)
        predicted_class = labels_jenis[np.argmax(predictions)]
        confidence = float(np.max(predictions))

        probs_dict = {
            labels_jenis[i]: float(predictions[0][i])
            for i in range(len(labels_jenis))
        }
        print("📊 Probabilitas:", probs_dict)
        print(f"🎯 Prediksi: {predicted_class} ({confidence:.4f})")

        insert_history("jenis", predicted_class, confidence, file.filename)

        return jsonify({
            "status": "success",
            "predicted": predicted_class,
            "confidence": confidence,
            "probabilities": probs_dict
        }), 200     

    except Exception as e:
        print("❌ Error saat deteksi jenis:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500

