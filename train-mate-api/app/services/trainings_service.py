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

from firebase_setup import db
from collections import Counter
from datetime import datetime

from collections import Counter
from firebase_setup import db

def get_popular_exercises():
    try:
        # Acceder a todos los documentos en la colección `trainings`
        trainings_ref = db.collection_group('user_trainings')  # Esto accede a todos los user_trainings de todos los usuarios
        trainings = trainings_ref.stream()

        # Crear un contador para contar la frecuencia de cada ejercicio
        exercise_counter = Counter()

        # Recorrer todos los entrenamientos y contar los ejercicios
        for training in trainings:
            training_data = training.to_dict()
            exercise_ids = training_data.get('exercises', [])
            
            # Contar cuántas veces aparece cada ejercicio
            for exercise_id in exercise_ids:
                # Asegurarse de que el ejercicio es público
                exercise_doc = db.collection('exercises').document(exercise_id).get()
                if exercise_doc.exists:
                    exercise_data = exercise_doc.to_dict()
                    if exercise_data.get('public', False):  # Solo contar ejercicios públicos
                        exercise_counter[exercise_id] += 1

        # Obtener los 5 ejercicios más populares
        most_common_exercises = exercise_counter.most_common(5)

        # Formatear los resultados para devolver ejercicio_id, nombre y cantidad de veces que lo hicieron
        popular_exercises = []
        for exercise_id, count in most_common_exercises:
            exercise_doc = db.collection('exercises').document(exercise_id).get()
            if exercise_doc.exists:
                exercise_data = exercise_doc.to_dict()
                popular_exercises.append({
                    'exercise_id': exercise_id,
                    'name': exercise_data.get('name'),
                    'count': count
                })

        return popular_exercises

    except Exception as e:
        print(f"Error getting popular exercises: {e}")
        return []
