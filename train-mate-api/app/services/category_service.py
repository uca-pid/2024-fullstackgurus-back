from firebase_setup import db

# Guardar categoría
def save_category(name, icon, isCustom, owner):
    try:
        category_ref = db.collection('categories').document()  # Crear una nueva categoría
        category_data = {
            'name': name,
            'icon': icon,
            'isCustom': isCustom,
            'owner': owner
        }
        category_ref.set(category_data)
        return True, category_ref.id  # Retornar el ID generado
    except Exception as e:
        print(f"Error saving category in Firestore: {e}")
        return False, None

# Obtener categorías (públicas y del usuario)
def get_categories(uid):
    try:
        categories_ref = db.collection('categories').where('owner', '==', uid).stream()
        return categories_ref
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return []
    
    
def get_category_by_id(uid, category_id):
    try:
        category_ref = db.collection('categories').document(category_id)
        category = category_ref.get()

        if not category.exists or (category.to_dict().get('owner') != uid and category.to_dict().get('owner') is not None):
            return None

        return category
    except Exception as e:
        print(f"Error fetching category by ID: {e}")
        return None



# Eliminar categoría
def delete_category(uid, category_id):
    try:
        category_ref = db.collection('categories').document(category_id)
        category = category_ref.get()

        if not category.exists or category.to_dict().get('owner') != uid:
            return False

        category_ref.delete()
        return True

    except Exception as e:
        print(f"Error deleting category in Firestore: {e}")
        return False

# Actualizar categoría
def update_category(uid, category_id, update_data):
    try:
        category_ref = db.collection('categories').document(category_id)
        category = category_ref.get()

        if not category.exists or category.to_dict().get('owner') != uid:
            return False

        category_ref.update(update_data)
        return True

    except Exception as e:
        print(f"Error updating category in Firestore: {e}")
        return False
