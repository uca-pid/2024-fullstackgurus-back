from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_token_service
from app.services.goals_service import complete_goal_service, get_all_goals_service, create_goal_service, get_goal_service, update_goal_service, delete_goal_service

goals_bp = Blueprint('goals_bp', __name__)

# Endpoint to get all goals for a user
@goals_bp.route('/get-all-goals', methods=['GET'])
def get_all_goals():
    try:
        # Verify the authorization token
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        goals = get_all_goals_service(uid)
        if goals is None:
            return jsonify({"error": "Failed to get goals"}), 500

        return jsonify(goals), 200

    except Exception as e:
        print(f"Error getting goals list: {e}")
        return jsonify({"error": "Something went wrong"}), 500


# Endpoint to create a new goal
@goals_bp.route('/create-goal', methods=['POST'])
def create_goal():
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        goal = create_goal_service(uid, data)
        
        # Check if goal creation failed due to invalid data
        if isinstance(goal, tuple) and goal[1] == 400:
            return jsonify(goal[0]), 400

        if not goal:
            return jsonify({"error": "Failed to create goal"}), 500

        return jsonify(goal), 201

    except Exception as e:
        print(f"Error creating goal: {e}")
        return jsonify({"error": "Something went wrong"}), 500



# Endpoint to get a specific goal
@goals_bp.route('/get-goal/<goal_id>', methods=['GET'])
def get_goal(goal_id):
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        goal = get_goal_service(uid, goal_id)
        if not goal:
            return jsonify({"error": "Goal not found"}), 404

        return jsonify(goal), 200

    except Exception as e:
        print(f"Error getting goal: {e}")
        return jsonify({"error": "Something went wrong"}), 500


# Endpoint to update a goal
@goals_bp.route('/update-goal/<goal_id>', methods=['PUT'])
def update_goal(goal_id):
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        updated_goal = update_goal_service(uid, goal_id, data)
        if not updated_goal:
            return jsonify({"error": "Failed to update goal"}), 500

        return jsonify(updated_goal), 200

    except Exception as e:
        print(f"Error updating goal: {e}")
        return jsonify({"error": "Something went wrong"}), 500


# Endpoint to delete a goal
@goals_bp.route('/delete-goal/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        if not delete_goal_service(uid, goal_id):
            return jsonify({"error": "Failed to delete goal"}), 500

        return jsonify({"message": "Goal deleted successfully"}), 200

    except Exception as e:
        print(f"Error deleting goal: {e}")
        return jsonify({"error": "Something went wrong"}), 500


@goals_bp.route('/complete-goal/<goal_id>', methods=['PATCH'])
def complete_goal(goal_id):
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403

        token = token.split(' ')[1]
        uid = verify_token_service(token)
        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        completed_goal = complete_goal_service(uid, goal_id)
        if not completed_goal:
            return jsonify({"error": "Failed to mark goal as completed"}), 500

        return jsonify(completed_goal), 200

    except Exception as e:
        print(f"Error completing goal: {e}")
        return jsonify({"error": "Something went wrong"}), 500
