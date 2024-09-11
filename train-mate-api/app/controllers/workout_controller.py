from flask import Blueprint, request, jsonify
from app.model.exercise import ExerciseType
from app.services.user_service import verify_token_service
from app.services.workout_service import save_user_workout, get_user_workouts, get_user_calories_from_workouts

workout_bp = Blueprint('workout_bp', __name__)

@workout_bp.route('/save-workout', methods=['POST'])
def record_workout():
    try:
        # Extract and validate the token
        token = request.headers.get('Authorization').split(' ')[1]

        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Token inválido'}), 401

        # Get request data
        data = request.get_json()

        # Validate the exercise type
        if data['exercise'] not in [exercise.value for exercise in ExerciseType]:
            return jsonify({'error': 'Invalid exercise type'}), 400

        # Save the workout and get the saved workout data
        saved_workout = save_user_workout(uid, data)

        # Return the saved workout as JSON
        return jsonify({
            'message': 'Entrenamiento guardado correctamente',
            'workout': saved_workout  # Include the saved workout in the response
        }), 201

    except Exception as e:
        print(e)
        return jsonify({'error': 'Algo salió mal'}), 500
    

@workout_bp.route('/workouts', methods=['GET'])
def get_workouts():
    try:
        # Extract and validate the token
        token = request.headers.get('Authorization').split(' ')[1]

        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Token inválido'}), 401

        # Get all workouts for the user
        workouts = get_user_workouts(uid)

        # Return the list of workouts
        return jsonify({
            'workouts': workouts
        }), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Algo salió mal'}), 500

@workout_bp.route('/get-workouts-calories', methods=['GET'])
def get_workouts_calories():
    try:
        # Extract and validate the token
        token = request.headers.get('Authorization').split(' ')[1]

        uid = verify_token_service(token)
        if uid is None:
            return jsonify({'error': 'Token inválido'}), 401

        # Get all workouts for the user
        workouts_calories, workouts_dates = get_user_calories_from_workouts(uid)

        # Return the list of workouts
        return jsonify({
            'workouts_calories': workouts_calories,
            'workouts_dates': workouts_dates
        }), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Algo salió mal'}), 500
