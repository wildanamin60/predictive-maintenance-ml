from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load model dan scaler saat server start
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'model_rf.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.pkl'))

# Mapping tipe produk
TYPE_MAP = {'L': 0, 'M': 1, 'H': 2}

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Ambil dan validasi input
        product_type = data.get('type', 'L')
        air_temp     = float(data.get('air_temperature', 0))
        proc_temp    = float(data.get('process_temperature', 0))
        rot_speed    = float(data.get('rotational_speed', 0))
        torque       = float(data.get('torque', 0))
        tool_wear    = float(data.get('tool_wear', 0))

        # Encode tipe produk
        type_encoded = TYPE_MAP.get(product_type.upper(), 0)

        # Susun input array sesuai urutan fitur waktu training
        input_data = np.array([[
            type_encoded,
            air_temp,
            proc_temp,
            rot_speed,
            torque,
            tool_wear
        ]])

        # Scaling
        input_scaled = scaler.transform(input_data)

        # Prediksi
        prediction = int(model.predict(input_scaled)[0])
        probability = model.predict_proba(input_scaled)[0].tolist()

        return jsonify({
            'success': True,
            'prediction': prediction,
            'label': 'FAILURE' if prediction == 1 else 'NORMAL',
            'probability_normal': round(probability[0] * 100, 2),
            'probability_failure': round(probability[1] * 100, 2)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'API berjalan normal'})


if __name__ == '__main__':
    app.run(debug=True)
