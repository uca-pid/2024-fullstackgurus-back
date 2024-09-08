from flask import Blueprint, request, jsonify
from app.services.user_service import save_user_info_service, verify_token_service, get_user_info_service, update_user_info_service, delete_user_service

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/save-user-info', methods=['POST'])
def save_user_info():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Token inválido'}), 401

        data = request.get_json()
        save_user_info_service(uid, data)

        return jsonify({'message': 'Información guardada correctamente'}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': 'Algo salió mal'}), 500
    

@user_bp.route('/get-user-info', methods=['GET'])
def get_user_info():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Token inválido'}), 401

        user_info = get_user_info_service(uid)
        if user_info:
            return jsonify(user_info), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'error': 'Algo salió mal'}), 500


@user_bp.route('/update-user-info', methods=['PUT'])
def update_user_info():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Token inválido'}), 401

        data = request.get_json()
        update_user_info_service(uid, data)

        return jsonify({'message': 'Información actualizada correctamente'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Algo salió mal'}), 500


@user_bp.route('/delete-user', methods=['DELETE'])
def delete_user():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Token inválido'}), 401

        delete_user_service(uid)

        return jsonify({'message': 'Usuario eliminado correctamente'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Algo salió mal'}), 500
