
from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_token_service
from app.services.category_service import (
    save_category as save_category_service,
    get_categories as get_categories_service,
    delete_category as delete_category_service,
    update_category as update_category_service,
    get_category_by_id as get_category_by_id_service
)

category_bp = Blueprint('category_bp', __name__)

# Valida la estructura y los datos de la categoría
def validate_category(data):
    name = data.get('name')
    icon = data.get('icon')
    isCustom = data.get('isCustom')

    if not name or not icon or isCustom is None:
        return {"error": "Missing data"}, 400

    if not isinstance(name, str) or not isinstance(icon, str) or not isinstance(isCustom, bool):
        return {"error": "Invalid data types"}, 400

    return None

# Guardar una categoría
@category_bp.route('/save-category', methods=['POST'])
def save_category():
    try:
        data = request.get_json()

        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        validation_error = validate_category(data)
        if validation_error:
            return jsonify(validation_error[0]), validation_error[1]

        if not uid and data.get('isCustom'):
            return jsonify({"error": "Invalid token for custom category"}), 403

        name = data['name']
        icon = data['icon']
        isCustom = data['isCustom']
        owner = uid if isCustom else None

        success, category_id = save_category_service(name, icon, isCustom, owner)
        if not success:
            return jsonify({"error": "Failed to save category"}), 500

        return jsonify({"message": "Category saved successfully", "category_id": category_id}), 201

    except Exception as e:
        print(f"Error saving category: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Obtener categorías
@category_bp.route('/get-categories', methods=['GET'])
def get_categories():
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        categories = get_categories_service(uid)
        
        # Add category_id to the returned data
        categories_with_id = []
        for category in categories:
            category_data = category.to_dict()
            category_data['category_id'] = category.id
            categories_with_id.append(category_data)
        
        return jsonify({"categories": categories_with_id}), 200

    except Exception as e:
        print(f"Error fetching categories: {e}")
        return jsonify({"error": "Something went wrong"}), 500


# Eliminar categoría
@category_bp.route('/delete-category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        success = delete_category_service(uid, category_id)
        if not success:
            return jsonify({"error": "Failed to delete category"}), 404

        return jsonify({"message": "Category deleted successfully"}), 200

    except Exception as e:
        print(f"Error deleting category: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Editar categoría
@category_bp.route('/edit-category/<category_id>', methods=['PUT'])
def edit_category(category_id):
    try:
        data = request.get_json()
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        update_data = {}
        
        if 'name' in data:
            if isinstance(data['name'], str):
                update_data['name'] = data['name']
            else:
                return jsonify({"error": "Invalid data type for 'name'"}), 400

        if 'icon' in data:
            if isinstance(data['icon'], str):
                update_data['icon'] = data['icon']
            else:
                return jsonify({"error": "Invalid data type for 'icon'"}), 400

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        success = update_category_service(uid, category_id, update_data)
        if not success:
            return jsonify({"error": "Failed to update category"}), 404

        return jsonify({"message": "Category updated successfully"}), 200

    except Exception as e:
        print(f"Error updating category: {e}")
        return jsonify({"error": "Something went wrong"}), 500
    
@category_bp.route('/get-category/<category_id>', methods=['GET'])
def get_category_by_id(category_id):
    try:
        token = request.headers.get('Authorization')
        if not token or 'Bearer ' not in token:
            return jsonify({"error": "Authorization token missing"}), 403
        
        token = token.split(' ')[1]
        uid = verify_token_service(token)

        if not uid:
            return jsonify({"error": "Invalid token"}), 403

        category = get_category_by_id_service(uid, category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        category_data = category.to_dict()
        category_data['category_id'] = category.id

        return jsonify(category_data), 200

    except Exception as e:
        print(f"Error fetching category by ID: {e}")
        return jsonify({"error": "Something went wrong"}), 500


# Guardar una categoría pública/default
@category_bp.route('/save-default-category', methods=['POST'])
def save_default_category():
    try:
        data = request.get_json()

        validation_error = validate_category(data)
        if validation_error:
            return jsonify(validation_error[0]), validation_error[1]

        name = data['name']
        icon = data['icon']
        isCustom = data['isCustom']
        owner = None

        success, category_id = save_category_service(name, icon, isCustom, owner)
        if not success:
            return jsonify({"error": "Failed to save category"}), 500

        return jsonify({"message": "Category saved successfully", "category_id": category_id}), 201

    except Exception as e:
        print(f"Error saving category: {e}")
        return jsonify({"error": "Something went wrong"}), 500