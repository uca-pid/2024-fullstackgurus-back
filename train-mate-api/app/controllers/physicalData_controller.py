from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_token_service
from app.services.physicalData_service import (
    add_physical_data_service,
    get_physical_data_service
)
from datetime import datetime

physicalData_bp = Blueprint('physicalData_bp', __name__)

@physicalData_bp.route('/add', methods=['POST'])
def add_physical_data():
    try:
        # Obtener el token de autorización y verificar el usuario
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        # Obtener los datos del body
        data = request.get_json()
        weight = data.get('weight')
        body_fat = data.get('body_fat')
        body_muscle = data.get('body_muscle')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))  # Si no envían fecha, usar la actual

        if not weight or not body_fat or not body_muscle:
            return jsonify({"error": "Missing parameters"}), 400

        success = add_physical_data_service(uid, body_fat, body_muscle, weight, date)
        if not success:
            return jsonify({"error": "Failed to save physical data"}), 500

        return jsonify({"message": "Physical data added successfully"}), 201

    except Exception as e:
        print(f"Error adding physical data: {e}")
        return jsonify({"error": "Something went wrong"}), 500

@physicalData_bp.route('/get-physical-data', methods=['GET'])
def get_physical_data():
    try:
        # Obtener el token de autorización y verificar el usuario
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        physical_data = get_physical_data_service(uid)
        if not physical_data:
            return jsonify({"error": "Failed to get physical data"}), 500

        return jsonify(physical_data), 200

    except Exception as e:
        print(f"Error getting physical data: {e}")
        return jsonify({"error": "Something went wrong"}), 500
