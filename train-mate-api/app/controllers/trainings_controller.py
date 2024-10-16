from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_token_service
from app.services.trainings_service import get_popular_exercises, save_user_training, get_user_trainings, get_training_by_id

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
            exercises_ids.append(exercise.get('id'))
        calories_per_hour_mean = round(calories_per_hour_sum / len(exercises))

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

@trainings_bp.route('/get-training/<training_id>', methods=['GET'])
def get_training_by_id(training_id):
    try:
        # Extract and validate the token
        token = request.headers.get('Authorization').split(' ')[1]
        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Invalid token'}), 401

        training = get_training_by_id(uid, training_id)
        if not training:
            return jsonify({'error': 'Training not found'}), 404

        return jsonify(training), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Something went wrong'}), 500
    

@trainings_bp.route('/popular-exercises', methods=['GET'])
def get_popular_exercises_view():
    try:
        
        # Get the top 5 exercises by popularity
        popular_exercises = get_popular_exercises()

        return jsonify({'popular_exercises': popular_exercises}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Something went wrong'}), 500