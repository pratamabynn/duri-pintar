from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
import numpy as np
from io import BytesIO
from db import insert_history

jenis_bp = Blueprint('jenis', __name__, url_prefix="/jenis")

print("🔄 Loading model jenis durian...")
model_jenis = load_model("Jenis durian fine tuning 2.h5")
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

durian_info = {
    "BENGKULU DURIAN": {
        "description": "Durian lokal dari Bengkulu dengan aroma kuat, daging tebal berwarna kuning pucat, dan rasa manis legit sedikit pahit.",
        "price_range": "Rp 50.000 - Rp 90.000 per kg"
    },
    "D24(SULTAN) DURIAN": {
        "description": "Dikenal sebagai 'Durian Sultan' dari Malaysia. Tekstur daging lembut, rasa manis berpadu pahit yang seimbang, sangat populer di pasaran premium.",
        "price_range": "Rp 150.000 - Rp 250.000 per kg"
    },
    "GOLDENPHOENIX DURIAN": {
        "description": "Varietas asal Malaysia dengan daging berwarna kuning pucat dan aroma tidak terlalu tajam. Rasanya manis-pahit dengan tekstur lembut.",
        "price_range": "Rp 180.000 - Rp 280.000 per kg"
    },
    "KOTA AGUNG DURIAN": {
        "description": "Durian unggulan dari Tanggamus, Lampung. Daging buah tebal berwarna kuning cerah, rasa manis gurih, dan aroma khas yang tidak terlalu menyengat.",
        "price_range": "Rp 60.000 - Rp 120.000 per kg"
    },
    "MEDAN DURIAN": {
        "description": "Durian populer di Indonesia dengan tekstur lembut, rasa manis legit, dan aroma tajam yang kuat. Sering dijadikan bahan olahan seperti pancake durian.",
        "price_range": "Rp 70.000 - Rp 150.000 per kg"
    },
    "MUSANG KING DURIAN": {
        "description": "Durian premium asal Malaysia dengan daging kuning keemasan, tekstur creamy, dan rasa manis-pahit khas. Termasuk jenis paling mahal dan dicari.",
        "price_range": "Rp 200.000 - Rp 400.000 per kg"
    },
    "SUMATRA SUPER DURIAN": {
        "description": "Varietas lokal unggulan dari Sumatra dengan daging tebal dan rasa manis gurih. Tekstur sedikit kering dan aroma sedang.",
        "price_range": "Rp 80.000 - Rp 130.000 per kg"
    }
}

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
        print(f"🎯 Prediksi: {predicted_class} ({confidence:.4f})")

        info = durian_info.get(predicted_class, {
            "description": "Informasi deskripsi tidak tersedia.",
            "price_range": "Tidak diketahui"
        })

        insert_history("jenis", predicted_class, confidence, file.filename)

        return jsonify({
            "status": "success",
            "predicted": predicted_class,
            "confidence": confidence,
            "description": info["description"],
            "price_range": info["price_range"],
        }), 200

    except Exception as e:
        print("❌ Error saat deteksi jenis:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500
