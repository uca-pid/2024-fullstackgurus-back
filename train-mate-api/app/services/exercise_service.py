from firebase_setup import db

# Save Exercise
def save_exercise(uid, name, calories_per_hour, public, category_id, training_muscle, image_url):
    try:
        exercise_ref = db.collection('exercises').document()  # Create a new document with a generated ID
        exercise_data = {
            'name': name,
            'calories_per_hour': calories_per_hour,
            'public': public,
            'owner': uid,
            'category_id': category_id,
            'image_url': image_url,
            'training_muscle': training_muscle
        }
        exercise_ref.set(exercise_data)
        exercise_data['id'] = exercise_ref.id
        return True, exercise_data
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

        return [{"id": exercise.id, **exercise.to_dict()} for exercise in exercises]  # Añadimos el exercise_id

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

# Get all excercices that exist, even if public or private, for the app integration
def get_all_exercises():
    try:
        exercises_ref = db.collection('exercises')
        exercises = exercises_ref.stream()
        return [
            {
                "id": exercise.id,  # Añadimos el id del ejercicio
                "calories_per_hour": exercise.get("calories_per_hour"),
                "name": exercise.get("name"),
                "public": exercise.get("public")
            }
            for exercise in exercises  # No es necesario hacer to_dict antes
        ]

    except Exception as e:
        print(f"Error getting all exercises: {e}")
        return []

def get_exercise_by_category_id(category_id, uid):
    try:
        exercises_ref = db.collection('exercises')
        exercises = exercises_ref.where('category_id', '==', category_id).where('owner', 'in', [uid, 'default']).stream()
        exercises_with_id = [{**exercise.to_dict(), 'id': exercise.id } for exercise in exercises]
        return exercises_with_id

    except Exception as e:
        print(f"Error getting exercises by category ID: {e}")
        return []


def get_exercise_by_id_service(exercise_id):
    try:
        # Fetch the exercise from the database using the exercise ID
        exercise_ref = db.collection('exercises').document(exercise_id)
        exercise_doc = exercise_ref.get()

        if not exercise_doc.exists:
            return None

        return exercise_doc.to_dict()

    except Exception as e:
        print(f"Error fetching exercise by ID: {e}")
        return None