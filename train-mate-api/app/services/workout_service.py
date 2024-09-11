from firebase_admin import auth
from firebase_setup import db
from app.services.user_service import get_user_info_service

def save_user_workout(uid, data):

    user_info = get_user_info_service(uid)

    # Check if user info exists and get the weight
    if not user_info or 'weight' not in user_info:
        raise ValueError("User information is incomplete. Weight is required.")
    
    calories = calculate_calories(data['exercise'], data['duration'], user_info['weight'])

    user_ref = db.collection('workouts').document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        user_ref.set({})

    # Reference to the user's workouts subcollection
    user_workouts_ref = db.collection('workouts').document(uid).collection('user_workouts')

    # Add a new document to the subcollection (Firestore generates a unique ID)
    workout_ref = user_workouts_ref.add({
        'exercise': data['exercise'],
        'duration': data['duration'],
        'date': data['date'],
        'calories': calories
    })

    # The workout_ref contains the Firestore-generated ID
    workout_id = workout_ref[1].id  # Access the ID of the newly created workout document

    # Return the workout data, including the ID
    saved_workout = {
        'id': workout_id,
        'exercise': data['exercise'],
        'duration': data['duration'],
        'date': data['date'],
        'calories': calories
    }

    return saved_workout

def get_user_workouts(uid):
    # Reference to the user's workouts subcollection
    user_workouts_ref = db.collection('workouts').document(uid).collection('user_workouts')

    # Get all documents from the subcollection
    workouts = user_workouts_ref.stream()

    # Parse each document and store it in a list
    workout_list = []
    for workout in workouts:
        workout_data = workout.to_dict()
        workout_data['id'] = workout.id  # Include the document ID in the response
        workout_list.append(workout_data)

    return workout_list

MET_VALUES = {
    'Running': 12.5,
    'Weightlifting': 6.0,
    'Cycling': 10.0,
    'Swimming': 7.0,
    'Football': 7.0,
    'Basketball': 8.0,
    'Tennis': 4.0,

}

def calculate_calories(exercise, duration, weight):
    # Get the MET value for the given exercise
    met_value = MET_VALUES.get(exercise, 0)  # Default to 0 if exercise is not in the list
    
    # Calculate calories burned using the formula
    calories_burned = (met_value * 3.5 * weight * duration) / 200
    
    return round(calories_burned, 2)  # Round to 2 decimal places for better readability
