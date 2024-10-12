from firebase_setup import db
import json

def save_user_training(uid, data, exercises_ids, calories_per_hour_mean):
    user_ref = db.collection('trainings').document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        user_ref.set({})

    user_trainings_ref = db.collection('trainings').document(uid).collection('user_trainings')

    training_ref = user_trainings_ref.add({
        'calories_per_hour_mean': calories_per_hour_mean,
        'exercises': exercises_ids,
        'name': data['name'],
        'owner': uid
    })

    training_id = training_ref[1].id

    saved_training = {
        'id': training_id,
        'calories_per_hour_mean': calories_per_hour_mean,
        'exercises': exercises_ids,
        'owner': uid,
    }

    return saved_training

def get_user_trainings(uid):

    user_trainings_ref = db.collection('trainings').document(uid).collection('user_trainings')

    try:
        trainings = user_trainings_ref.stream()
        training_list = []
        for training in trainings:
            training_data = training.to_dict()
            exercise_ids = training_data.get('exercises', [])
            training_data['exercises'] = []
            for exercise_id in exercise_ids:
                exercise_doc = db.collection('exercises').document(exercise_id).get()
                if exercise_doc.exists:
                    exercise_data = exercise_doc.to_dict()
                    exercise_data['exercise_id'] = exercise_id
                    training_data['exercises'].append(exercise_data)
            training_data['id'] = training.id
            training_list.append(training_data)
        return training_list

    except Exception as e:
        print(f"Error getting trainings from Firestore: {e}")
        return []

def get_training_by_id(uid, training_id):
    training_ref = db.collection('trainings').document(uid).collection('user_trainings').document(training_id)
    training = training_ref.get()

    if not training.exists:
        return None

    training_data = training.to_dict()
    return training_data