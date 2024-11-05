from firebase_setup import db

def get_challenges_list_service(uid, type):
    try:
        user_ref = db.collection('challenges').document(uid)
        user_doc = user_ref.get()

        # Si el documento no existe, lo creamos
        if not user_doc.exists:
            user_ref.set({})

        if type == 'physical':
            challenges = user_ref.collection('user_physical_challenges').stream()
        
        elif type == 'trainings':
            challenges = user_ref.collection('user_trainings_challenges').stream()

        elif type == 'workouts':
            challenges = user_ref.collection('user_workouts_challenges').stream()
        
        else:
            print(f"Invalid type: {type}")
            return None

        challenges_list = []
        for challenge in challenges:
            challenges_data = challenge.to_dict()
            challenges_data['id'] = challenge.id
            challenges_list.append(challenges_data)
    
    except Exception as e:
        print(f"Error getting challenges: {e}")

    return challenges_list