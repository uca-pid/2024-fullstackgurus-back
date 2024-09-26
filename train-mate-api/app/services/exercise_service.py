from firebase_setup import db

# Save Exercise
def save_exercise(uid, name, calories_per_hour, public):
    try:
        exercise_ref = db.collection('exercises').document()  # Create a new document with a generated ID
        exercise_data = {
            'name': name,
            'calories_per_hour': calories_per_hour,
            'public': public,
            'owner': uid
        }
        exercise_ref.set(exercise_data)  # Save the data
        return exercise_ref.id  # Return the generated ID
    except Exception as e:
        print(f"Error saving exercise in Firestore: {e}")
        return None

# Get Exercises (User-specific, with optional public filter)
def get_exercises(uid, show_public):
    try:
        exercises_ref = db.collection('exercises')
        if show_public:
            # Fetch all public exercises
            exercises = exercises_ref.where('public', '==', True).stream()
        else:
            # Fetch exercises created by the user
            exercises = exercises_ref.where('owner', '==', uid).stream()

        return [exercise.to_dict() for exercise in exercises]

    except Exception as e:
        print(f"Error getting exercises from Firestore: {e}")
        return []

# Delete Exercise
def delete_exercise(uid, exercise_id):
    try:
        exercise_ref = db.collection('exercises').document(exercise_id)
        exercise = exercise_ref.get()

        if not exercise.exists or exercise.to_dict().get('owner') != uid:
            return False

        exercise_ref.delete()
        return True

    except Exception as e:
        print(f"Error deleting exercise in Firestore: {e}")
        return False

# Update Exercise
def update_exercise(uid, exercise_id, update_data):
    try:
        exercise_ref = db.collection('exercises').document(exercise_id)
        exercise = exercise_ref.get()

        if not exercise.exists or exercise.to_dict().get('owner') != uid:
            return False

        exercise_ref.update(update_data)
        return True

    except Exception as e:
        print(f"Error updating exercise in Firestore: {e}")
        return False
