from firebase_setup import db
from datetime import datetime
from app.services.checkChallenges_service import check_and_update_physical_challenges

def add_physical_data_service(uid, body_fat, body_muscle, weight, date):
    try:
        # Referencia al documento del usuario
        user_ref = db.collection('physical_data').document(uid)
        user_doc = user_ref.get()

        # Si el documento no existe, lo creamos
        if not user_doc.exists:
            user_ref.set({})

        physical_data_ref = user_ref.collection('user_physical_data').document(date)

        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_obj = date_obj.replace(hour=10, minute=0)

        physical_data_ref.set({
            'weight': weight,
            'date': date_obj,
            'body_fat': body_fat,
            'body_muscle': body_muscle,
        })
        
        check_and_update_physical_challenges(uid, date)

        return True

    except Exception as e:
        print(f"Error saving physical data: {e}")
        return False

def get_physical_data_service(uid):
    try:
        physical_data = []
        user_ref = db.collection('physical_data').document(uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return physical_data

        physical_data_ref = user_ref.collection('user_physical_data').stream()

        for data in physical_data_ref:
            physical_data.append(data.to_dict())

        return physical_data

    except Exception as e:
        print(f"Error getting physical data: {e}")
        return False