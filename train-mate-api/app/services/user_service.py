from firebase_admin import auth
from firebase_setup import db

def verify_token_service(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception as e:
        print(e)
        return None

def save_user_info_service(uid, data):
    user_ref = db.collection('users').document(uid)
    
    # Crear el diccionario solo con los valores que no sean None
    user_data = {}
    
    if 'email' in data and data['email'] is not None:
        user_data['email'] = data['email']
        
    if 'name' in data and data['name'] is not None:
        user_data['fullName'] = data['name']
        
    if 'sex' in data and data['sex'] is not None:
        user_data['gender'] = data['sex']
        
    if 'weight' in data and data['weight'] is not None:
        user_data['weight'] = data['weight']
        
    if 'height' in data and data['height'] is not None:
        user_data['height'] = data['height']
        
    if 'birthday' in data and data['birthday'] is not None:
        user_data['birthday'] = data['birthday']

    # Guardar solo si hay datos válidos
    if user_data:
        user_ref.set(user_data)
    else:
        print(f"No hay datos válidos para guardar para el usuario {uid}.")

def get_user_info_service(uid):
    user_ref = db.collection('users').document(uid)
    user_doc = user_ref.get()

    if user_doc.exists:
        return user_doc.to_dict()
    else:
        print(f"Usuario con UID {uid} no encontrado. Creando un nuevo usuario...")
        user = auth.get_user(uid)
        email = user.email
        save_user_info_service(uid, {'email': email})
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()
        return user_doc.to_dict()

def update_user_info_service(uid, data):
    user_ref = db.collection('users').document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        print(f"Usuario con UID {uid} no encontrado. Creando un nuevo usuario...")
        save_user_info_service(uid, data)
        return

    update_data = {}
    
    if 'full_name' in data and data['full_name'] is not None:
        update_data['fullName'] = data['full_name']
    
    if 'gender' in data and data['gender'] is not None:
        update_data['gender'] = data['gender']
    
    if 'weight' in data and data['weight'] is not None:
        update_data['weight'] = data['weight']
    
    if 'height' in data and data['height'] is not None:
        update_data['height'] = data['height']

    if 'birthday' in data and data['birthday'] is not None:
        update_data['birthday'] = data['birthday']

    if update_data:
        user_ref.update(update_data)

def delete_user_service(uid):
    user_ref = db.collection('users').document(uid)
    user_ref.delete()
