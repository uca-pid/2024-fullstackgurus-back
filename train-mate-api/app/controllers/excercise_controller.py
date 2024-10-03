from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_token_service
from app.services.exercise_service import (
    save_exercise as save_exercise_service,
    get_exercises as get_exercises_service,
    delete_exercise as delete_exercise_service,
    update_exercise as update_exercise_service,
    get_all_exercises as get_all_exercises_service,
    get_exercise_by_category_id as get_exercise_by_category_id_service,
)

exercise_bp = Blueprint('exercise_bp', __name__)

def validate_body(data):
    name = data.get('name')
    calories_per_hour = data.get('calories_per_hour')
    public = data.get('public')
    category_id = data.get('category_id')

    if not name or calories_per_hour is None or public is None or category_id is None:
        return {"error": "Missing data"}, 400

    if not isinstance(name, str) or not isinstance(calories_per_hour, (int, float)) or not isinstance(public, (str, bool)):
        return {"error": "Invalid data types"}, 400

    if calories_per_hour <= 0 or calories_per_hour >= 10000:
        return {"error": "calorias_por_hora should be between 1 and 10000"}, 400

    return None

# Save Exercise
@exercise_bp.route('/save-exercise', methods=['POST'])
def save_exercise():
    try:
        data = request.get_json()
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        validation_error = validate_body(data)
        if validation_error:
            return jsonify(validation_error[0]), validation_error[1]

        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        name = data['name']
        calories_per_hour = data['calories_per_hour']
        public = data['public']
        category_id = data['category_id']

        if isinstance(public, str):
            public = True if public.lower() == 'true' else False

        success, exercise = save_exercise_service(uid, name, calories_per_hour, public, category_id)
        if not success:
            return jsonify({"error": "Failed to save exercise"}), 500

        return jsonify({"message": "Exercise saved successfully", "exercise": exercise}), 201

    except Exception as e:
        print(f"Error saving exercise: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Get Exercises
@exercise_bp.route('/get-exercises', methods=['GET'])
def get_exercises():
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        show_public = request.args.get('public', 'false').lower() == 'true'
        exercises = get_exercises_service(uid, show_public)
        return jsonify({"exercises": exercises}), 200

    except Exception as e:
        print(f"Error fetching exercises: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Delete Exercise
@exercise_bp.route('/delete-exercise/<exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        success = delete_exercise_service(uid, exercise_id)
        if not success:
            return jsonify({"error": "Failed to delete exercise"}), 404

        return jsonify({"message": "Exercise deleted successfully"}), 200

    except Exception as e:
        print(f"Error deleting exercise: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Edit Exercise
@exercise_bp.route('/edit-exercise/<exercise_id>', methods=['PUT'])
def edit_exercise(exercise_id):
    try:
        data = request.get_json()
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        # En vez de usar una validación rígida, validamos si se envió cada campo
        update_data = {}
        
        if 'name' in data:
            name = data['name']
            if isinstance(name, str):
                update_data['name'] = name
            else:
                return jsonify({"error": "Invalid data type for 'name'"}), 400
        
        if 'calories_per_hour' in data:
            calories_per_hour = data['calories_per_hour']
            if isinstance(calories_per_hour, (int, float)) and 0 < calories_per_hour < 10000:
                update_data['calories_per_hour'] = calories_per_hour
            else:
                return jsonify({"error": "Invalid data type or value for 'calories_per_hour'"}), 400

        if 'public' in data:
            public = data['public']
            if isinstance(public, str):
                public = True if public.lower() == 'true' else False
            if isinstance(public, bool):
                update_data['public'] = public
            else:
                return jsonify({"error": "Invalid data type for 'public'"}), 400

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        success = update_exercise_service(uid, exercise_id, update_data)
        if not success:
            return jsonify({"error": "Failed to update exercise"}), 404

        return jsonify({"message": "Exercise updated successfully"}), 200

    except Exception as e:
        print(f"Error updating exercise: {e}")
        return jsonify({"error": "Something went wrong"}), 500


# Get All Exercises. Public endpoint
@exercise_bp.route('/get-all-exercises', methods=['GET'])
def get_all_exercises():
    try:
        exercises = get_all_exercises_service()
        return jsonify({"exercises": exercises}), 200

    except Exception as e:
        print(f"Error fetching exercises: {e}")
        return jsonify({"error": "Something went wrong"}), 500
    
# Save Exercise
@exercise_bp.route('/save-default-exercises', methods=['POST'])
def save_default_exercises():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "Input should be a list of exercises"}), 400

        response = []
        for exercise in data:
            validation_error = validate_body(exercise)
            if validation_error:
                response.append({"exercise": exercise, "error": validation_error[0]})
                continue

            name = exercise['name']
            calories_per_hour = exercise['calories_per_hour']
            public = exercise['public']
            category_id = exercise['category_id']
            uid = "default"

            if isinstance(public, str):
                public = True if public.lower() == 'true' else False

            success = save_exercise_service(uid, name, calories_per_hour, public, category_id)
            if not success:
                response.append({"exercise": exercise, "error": "Failed to save exercise"})
                continue

            response.append({"exercise": exercise, "message": "Exercise saved successfully"})

        return jsonify(response), 207

    except Exception as e:
        print(f"Error saving exercises: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Get Exercises by Category ID
@exercise_bp.route('/get-exercises-by-category/<category_id>', methods=['GET'])
def get_exercises_by_category_id(category_id):
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        if not uid:
            return jsonify({"error": "Invalid token"}), 403
        
        exercises = get_exercise_by_category_id_service(category_id)
        return jsonify({"exercises": exercises}), 200

    except Exception as e:
        print(f"Error fetching exercises: {e}")
        return jsonify({"error": "Something went wrong"}), 500
