from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_token_service
from app.services.trainings_service import save_user_training, get_user_trainings

trainings_bp = Blueprint('trainings_bp', __name__)

@trainings_bp.route('/save-training', methods=['POST'])
def save_training():
    try:
        # Extract and validate the token
        token = request.headers.get('Authorization').split(' ')[1]
        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Invalid token'}), 401

        # Get request data
        data = request.get_json()

        # Calculate calories per hour mean
        exercises = data.get('exercises')
        calories_per_hour_sum = 0
        exercises_ids = []
        for exercise in exercises:
            calories_per_hour_sum += exercise.get('calories_per_hour')
            exercises_ids.append(exercise.get('exercise_id'))
        calories_per_hour_mean = calories_per_hour_sum / len(exercises)

        saved_training = save_user_training(uid, data, exercises_ids, calories_per_hour_mean)

        return jsonify({
            'message': 'Training saved successfully',
            'training': saved_training
        }), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

@trainings_bp.route('/get-trainings', methods=['GET'])
def get_trainings():
    try:
        # Extract and validate the token
        token = request.headers.get('Authorization').split(' ')[1]
        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Invalid token'}), 401

        trainings = get_user_trainings(uid)
        return jsonify({'trainings': trainings}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Something went wrong'}), 500