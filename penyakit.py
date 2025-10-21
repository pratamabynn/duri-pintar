from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from db import insert_history

penyakit_bp = Blueprint('penyakit', __name__, url_prefix="/duri-pintar/penyakit")

print("🔄 Loading model penyakit...")
model = load_model("penyakit-durian.h5")
print("✅ Model penyakit berhasil dimuat.")

class_labels = ["ALGAL LEAF SPOT", "ALLOCARIDARA ATTACK", "HEALTHY LEAF", "LEAF BLIGHT", "PHOMOPSIS LEAF SPOT"]

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
                "confidence": confidence
            }), 200
        else:
            insert_history("penyakit", predicted_class, confidence, file.filename)
            return jsonify({
                "status": "success",
                "prediction": predicted_class,
                "confidence": confidence
            }), 200

    except Exception as e:
        print("❌ Error saat prediksi penyakit:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500

