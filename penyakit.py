from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from db import insert_history

penyakit_bp = Blueprint('penyakit', __name__, url_prefix="/penyakit")

print("🔄 Loading model penyakit...")
model = load_model("Durian fine tuning 2.h5")
print("✅ Model penyakit berhasil dimuat.")

class_labels = [
    "ALGAL LEAF SPOT",
    "ALLOCARIDARA ATTACK",
    "HEALTHY LEAF",
    "LEAF BLIGHT",
    "PHOMOPSIS LEAF SPOT"
]

penyakit_descriptions = {
    "ALGAL LEAF SPOT": "Penyakit yang disebabkan oleh alga hijau parasit (Cephaleuros virescens). Gejalanya berupa bercak hijau keabu-abuan di permukaan daun yang bisa berkembang menjadi coklat kemerahan.",
    "ALLOCARIDARA ATTACK": "Serangan serangga *Allocaridara malayensis* yang biasanya menyebabkan bercak kuning atau lubang kecil pada daun akibat aktivitas mengisap cairan daun.",
    "HEALTHY LEAF": "Daun dalam kondisi sehat tanpa tanda-tanda penyakit atau serangan hama. Warna daun hijau merata dan permukaan bersih.",
    "LEAF BLIGHT": "Penyakit hawar daun yang disebabkan oleh jamur. Menyebabkan tepi daun mengering, bercak coklat kehitaman, dan akhirnya daun gugur.",
    "PHOMOPSIS LEAF SPOT": "Infeksi jamur *Phomopsis sp.* yang menimbulkan bercak kecil berwarna coklat dengan tepi kekuningan. Penyakit ini dapat menyebabkan daun mengering dan rontok prematur."
}

@penyakit_bp.route('/predict', methods=['POST'])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "File tidak ditemukan"}), 400
        
        file = request.files['file']
        file.stream.seek(0)

        img = image.load_img(BytesIO(file.read()), target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions)
        predicted_class = class_labels[predicted_index]
        confidence = float(np.max(predictions))

        THRESHOLD = 0.8
        if confidence < THRESHOLD:
            insert_history("penyakit", "Bukan daun durian", confidence, file.filename)
            return jsonify({
                "status": "success",
                "prediction": "Bukan daun durian",
                "confidence": confidence,
                "description": "Gambar yang dikirim kemungkinan bukan daun durian atau kualitas gambar kurang jelas untuk dikenali."
            }), 200
        else:
            description = penyakit_descriptions.get(predicted_class, "Deskripsi tidak tersedia.")
            insert_history("penyakit", predicted_class, confidence, file.filename)
            return jsonify({
                "status": "success",
                "prediction": predicted_class,
                "confidence": confidence,
                "description": description
            }), 200

    except Exception as e:
        print("❌ Error saat prediksi penyakit:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500
