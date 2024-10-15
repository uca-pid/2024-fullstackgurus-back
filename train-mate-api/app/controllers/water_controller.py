from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_token_service
from app.services.water_service import (
    add_water_intake_service,
    get_daily_water_intake_service,
    get_water_intake_history_service
)
from datetime import datetime

water_bp = Blueprint('water_bp', __name__)

# Endpoint para cargar cuánta agua tomé
@water_bp.route('/add', methods=['POST'])
def add_water_intake():
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
        quantity_in_militers = data.get('quantity_in_militers')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))  # Si no envían fecha, usar la actual
        public = data.get('public', False)

        # Validar que se envió la cantidad de agua en mililitros
        if not quantity_in_militers:
            return jsonify({"error": "Invalid water quantity"}), 400

        # Llamar al servicio para guardar la ingesta de agua
        success = add_water_intake_service(uid, quantity_in_militers, date, public)
        if not success:
            return jsonify({"error": "Failed to save water intake"}), 500

        return jsonify({"message": "Water intake added successfully"}), 201

    except Exception as e:
        print(f"Error adding water intake: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Endpoint para ver cuánta agua tomé en el día
@water_bp.route('/get-daily-water-intake', methods=['GET'])
def get_daily_water_intake():
    try:
        # Obtener el token de autorización y verificar el usuario
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        # Llamar al servicio para obtener el agua del día
        date = datetime.now().strftime('%Y-%m-%d')
        daily_intake = get_daily_water_intake_service(uid, date)
        if daily_intake is None:
            return jsonify({"message": "No water intake found for today", "quantity_in_militers": 0}), 200

        return jsonify({"date": date, "quantity_in_militers": daily_intake}), 200

    except Exception as e:
        print(f"Error getting daily water intake: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Endpoint para obtener un historial de ingesta de agua en un rango de fechas
@water_bp.route('/get-water-intake-history', methods=['GET'])
def get_water_intake_history():
    try:
        # Obtener el token de autorización y verificar el usuario
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        # Obtener los parámetros de rango de fechas de la URL
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Start date and end date are required"}), 400

        # Llamar al servicio para obtener el historial de ingesta de agua
        history = get_water_intake_history_service(uid, start_date, end_date)

        return jsonify({"water_intake_history": history}), 200

    except Exception as e:
        print(f"Error getting water intake history: {e}")
        return jsonify({"error": "Something went wrong"}), 500
