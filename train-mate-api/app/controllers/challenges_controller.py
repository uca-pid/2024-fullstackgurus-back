from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_token_service
from app.services.challenges_service import get_challenges_list_service

challenges_bp = Blueprint('challenges_bp', __name__)

@challenges_bp.route('/get-challenges-list/<type>', methods=['GET']) 
def get_challenges_list(type):
    try:
        # Obtener el token de autorización y verificar el usuario
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        challenges = get_challenges_list_service(uid, type)
        if challenges is None:
            return jsonify({"error": "Failed to get challenges"}), 500

        return jsonify(challenges), 200

    except Exception as e:
        print(f"Error getting challenges list: {e}")
        return jsonify({"error": "Something went wrong"}), 500