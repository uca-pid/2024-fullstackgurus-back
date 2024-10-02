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
        except ValueError:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")
    else:
        date_obj = db.SERVER_TIMESTAMP

    # Reference to the user's workouts subcollection
    user_workouts_ref = db.collection('workouts').document(uid).collection('user_workouts')

    # Add a new document to the subcollection
    workout_ref = user_workouts_ref.add({
        'exercise_id': data['exercise_id'],
        'exercise': data['exercise'],
        'duration': data['duration'],
        'date': date_obj,
        'calories': calories_burned
    })

    # The workout_ref contains the Firestore-generated ID
    workout_id = workout_ref[1].id

    # Return the workout data, including the ID
    saved_workout = {
        'id': workout_id,
        'exercise_id': data['exercise_id'],
        'exercise': data['exercise'],
        'duration': data['duration'],
        'date': date_obj,
        'calories': calories_burned
    }

    return saved_workout


def get_user_workouts(uid, start_date=None, end_date=None):
    # Reference to the user's workouts subcollection
    user_workouts_ref = db.collection('workouts').document(uid).collection('user_workouts')


    try:
        # Filtrado por startDate si está presente
        if start_date:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            print("start date time", start_datetime)
            user_workouts_ref = user_workouts_ref.where('date', '>=', start_datetime)

        # Filtrado por endDate si está presente
        if end_date:
            print(end_date)
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
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
            print("start date time", start_datetime)
            user_workouts_ref = user_workouts_ref.where('date', '>=', start_datetime)

        # Filtrado por endDate si está presente
        if end_date:
            print(end_date)
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
    for workout in workouts:
        workout_data = workout.to_dict()
        workout_calories = workout_data['calories']
        workout_date = workout_data['date']
        workout_calories_list.append(workout_calories)
        workout_dates_list.append(workout_date)

    return workout_calories_list, workout_dates_list

# MET_VALUES = {
#     'Running': 12.5,
#     'Weightlifting': 6.0,
#     'Cycling': 10.0,
#     'Swimming': 7.0,
#     'Football': 7.0,
#     'Basketball': 8.0,
#     'Tennis': 4.0,

# }

# def calculate_calories(exercise, duration, weight):
#     # Get the MET value for the given exercise
#     met_value = MET_VALUES.get(exercise, 0)  # Default to 0 if exercise is not in the list
    
#     # Calculate calories burned using the formula
#     calories_burned = (met_value * 3.5 * weight * duration) / 200
    
#     return round(calories_burned, 2)  # Round to 2 decimal places for better readability
