from firebase_admin import auth
from firebase_admin import firestore
from firebase_setup import db
from app.services.user_service import get_user_info_service
from datetime import datetime

def save_user_workout(uid, data, calories_burned):
    user_ref = db.collection('workouts').document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        user_ref.set({})

    # Convert the date from string to a datetime object
    if 'date' in data and isinstance(data['date'], str):
        try:
            date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
            date_obj = date_obj.replace(hour=10, minute=0) # Set default time a las 10:00 AM porque sino por el uso horario Firebase te lo tira -3 horas al dia anterior
        except ValueError:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")
    else:
        date_obj = db.SERVER_TIMESTAMP

    # Reference to the user's workouts subcollection
    user_workouts_ref = db.collection('workouts').document(uid).collection('user_workouts')

    # Add a new document to the subcollection
    workout_ref = user_workouts_ref.add({
        'training_id': data['training_id'],
        'duration': data['duration'],
        'date': date_obj,
        'total_calories': calories_burned,
        'coach': data['coach']
    })

    # The workout_ref contains the Firestore-generated ID
    workout_id = workout_ref[1].id

    # Return the workout data, including the ID
    saved_workout = {
        'id': workout_id,
        'training_id': data['training_id'],
        'duration': data['duration'],
        'date': date_obj,
        'total_calories': calories_burned,
        'coach': data['coach']
    }

    return saved_workout


def get_user_workouts(uid, start_date=None, end_date=None):
    # Reference to the user's workouts subcollection
    user_workouts_ref = db.collection('workouts').document(uid).collection('user_workouts')

    try:
        # Filtrado por startDate si está presente
        if start_date:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            start_datetime = start_datetime.replace(hour=10, minute=0)
            user_workouts_ref = user_workouts_ref.where('date', '>=', start_datetime)

        # Filtrado por endDate si está presente
        if end_date:
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
            end_datetime = end_datetime.replace(hour=10, minute=0)
            user_workouts_ref = user_workouts_ref.where('date', '<=', end_datetime)

        # Obtener los workouts filtrados (o todos si no se pasa ningún filtro)
        workouts = user_workouts_ref.stream()

    except ValueError:
        return {"error": "Formato de fecha inválido. Usa 'YYYY-MM-DD'."}

    # Parse each document and store it in a list
    workout_list = []
    for workout in workouts:
        workout_data = workout.to_dict()
        workout_data['id'] = workout.id  # Include the document ID in the response
        workout_list.append(workout_data)

    return workout_list

def get_user_calories_from_workouts(uid, start_date=None, end_date=None):
    # Reference to the user's workouts subcollection
    user_workouts_ref = db.collection('workouts').document(uid).collection('user_workouts')

    try:
        # Filtrado por startDate si está presente
        if start_date:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            user_workouts_ref = user_workouts_ref.where('date', '>=', start_datetime)

        # Filtrado por endDate si está presente
        if end_date:
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
            user_workouts_ref = user_workouts_ref.where('date', '<=', end_datetime)

        # Obtener los workouts filtrados (o todos si no se pasa ningún filtro)
        workouts = user_workouts_ref.stream()

    except ValueError:
        return {"error": "Formato de fecha inválido. Usa 'YYYY-MM-DD'."}

    # Get all documents from the subcollection
    workouts = user_workouts_ref.stream()

    # Parse each document and store it in a list
    workout_calories_list = []
    workout_dates_list = []
    workout_training_id_list = []
    for workout in workouts:
        workout_data = workout.to_dict()
        workout_calories = workout_data['total_calories']
        workout_date = workout_data['date']
        workout_training_id = workout_data['training_id']
        workout_calories_list.append(workout_calories)
        workout_dates_list.append(workout_date)
        workout_training_id_list.append(workout_training_id)

    return workout_calories_list, workout_dates_list, workout_training_id_list



def delete_user_workout(uid, workout_id):
    # Reference to the specific workout document
    workout_ref = db.collection('workouts').document(uid).collection('user_workouts').document(workout_id)
    workout_doc = workout_ref.get()

    # Check if the workout exists
    if not workout_doc.exists:
        return {'error': 'Workout not found'}, 404

    # Check if the workout date is in the future
    workout_data = workout_doc.to_dict()
    workout_date = workout_data['date'].replace(tzinfo=None)  # Ensure no timezone for comparison

    if workout_date <= datetime.now():
        return {'error': 'Cannot cancel past workouts'}, 400

    # Delete the workout if it is scheduled for the future
    workout_ref.delete()
    return {'message': 'Workout cancelled successfully'}, 200