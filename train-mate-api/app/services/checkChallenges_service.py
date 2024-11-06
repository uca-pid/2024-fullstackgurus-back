from firebase_setup import db
from datetime import datetime, timedelta

def check_and_update_physical_challenges(uid, date):
    try:
        # References
        user_ref = db.collection('physical_data').document(uid)
        user_physical_data_ref = user_ref.collection('user_physical_data')
        user_challenges_ref = db.collection('challenges').document(uid).collection('user_physical_challenges')
        
        # Convert date string to datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        
        # Fetch past 30 days of data
        start_date = date_obj - timedelta(days=30)
        recent_entries = user_physical_data_ref.where('date', '>=', start_date).stream()
        
        # Calculate metrics
        entries = list(recent_entries)
        muscle_changes = [entry.get('body_muscle') for entry in entries]
        fat_changes = [entry.get('body_fat') for entry in entries]
        weight_changes = [entry.get('weight') for entry in entries]
        days_logged = len(entries)
        
        # Challenges states
        challenge_updates = {}
        # Challenge 1: Consistency is Key - 7 consecutive days
        if days_logged >= 7:
            entries.sort(key=lambda entry: entry.get('date').timestamp())
            consecutive_days = 0
            for i in range(len(entries) - 1):
                print(f"Date: {entries[i].get('date')}")
                if (entries[i + 1].get('date').timestamp() - entries[i].get('date').timestamp()) <= 86400:
                    consecutive_days += 1
                else:
                    consecutive_days = 0
                if consecutive_days >= 6:
                    challenge_updates['Consistency is Key'] = True
                    break 

        # Challenge 2: Muscle Up! - Increase muscle by 2 kg in a month
        if muscle_changes and (max(muscle_changes) - min(muscle_changes) >= 2):
            challenge_updates['Muscle Up!'] = True

        # Challenge 3: Fat Loss Focus - Decrease body fat by 1% in two weeks
        two_weeks_ago = date_obj - timedelta(days=14)
        two_week_entries = user_physical_data_ref.where('date', '>=', two_weeks_ago).stream()
        fat_changes_two_weeks = [entry.get('body_fat') for entry in two_week_entries]
        if fat_changes_two_weeks and (fat_changes_two_weeks[0] - fat_changes_two_weeks[-1] >= 1):
            challenge_updates['Fat Loss Focus'] = True

        # Challenge 4: Weight Watcher - Stable weight within 0.5 kg over a month
        if weight_changes and (max(weight_changes) - min(weight_changes) <= 0.5):
            challenge_updates['Weight Watcher'] = True

        # Challenge 5: Progress Pioneer - 30 entries within 60 days
        sixty_days_ago = date_obj - timedelta(days=60)
        entries_last_60_days = user_physical_data_ref.where('date', '>=', sixty_days_ago).stream()
        if len(list(entries_last_60_days)) >= 30:
            challenge_updates['Progress Pioneer'] = True

        # Update challenges in the database
        for challenge_name, completed in challenge_updates.items():
            if completed:
                challenge_docs = user_challenges_ref.where('challenge', '==', challenge_name).get()
                for doc in challenge_docs:
                    doc.reference.update({'state': True})

        return True

    except Exception as e:
        print(f"Error updating challenges: {e}")
        return False

def check_and_update_workouts_challenges(uid):
    try:
        # Reference to user's workout and challenge data
        user_workouts_ref = db.collection('workouts').document(uid).collection('user_workouts')
        user_challenges_ref = db.collection('challenges').document(uid).collection('user_workouts_challenges')
        
        # Fetch workouts in the last 30 days
        date_30_days_ago = datetime.now() - timedelta(days=30)
        recent_workouts = user_workouts_ref.where('date', '>=', date_30_days_ago).stream()
        workouts = list(recent_workouts)
        
        # Counters and accumulators
        category_count = {}
        coach_count = set()
        unique_exercises = set()
        total_calories = 0
        total_workouts = len(workouts)
        sports_duration = 0
        long_duration_workouts = 0
        
        # Process each workout
        for workout in workouts:
            data = workout.to_dict()
            total_calories += data.get('total_calories', 0)
            coach_count.add(data.get('coach'))
            if data.get('duration', 0) >= 120:
                long_duration_workouts += 1
            
            # Fetch training details
            training_id = data.get('training_id')
            training_ref = db.collection('trainings').document(training_id)
            training_doc = training_ref.get()
            if training_doc.exists:
                training_data = training_doc.to_dict()
                
                # Fetch exercises within the training
                exercises = training_data.get('exercises', [])
                for exercise_id in exercises:
                    exercise_ref = db.collection('exercises').document(exercise_id)
                    exercise_doc = exercise_ref.get()
                    if exercise_doc.exists:
                        exercise_data = exercise_doc.to_dict()
                        unique_exercises.add(exercise_data.get('name'))
                        
                        # Accumulate sports duration
                        category_id = exercise_data.get('category_id')
                        category_ref = db.collection('categories').document(category_id)
                        category_doc = category_ref.get()
                        if category_doc.exists:
                            category_data = category_doc.to_dict()
                            category_name = category_data.get('name')
                            category_count[category_name] = category_count.get(category_name, 0) + 1
                            
                            # Check if category is "Sports"
                            if category_name == "Sports":
                                sports_duration += data.get('duration', 0)
        
        # Challenge updates
        challenge_updates = {}

        # Challenge 1: Category Master
        if len(category_count) >= 5:
            challenge_updates["Category Master"] = True

        # Challenge 2: Endurance Streak
        if total_workouts >= 10 and all(
            (workouts[i + 1].to_dict().get('date') - workouts[i].to_dict().get('date')).days == 1 
            for i in range(len(workouts) - 1)
        ):
            challenge_updates["Endurance Streak"] = True

        # Challenge 3: Strength Specialist
        if category_count.get("Strength", 0) >= 20:
            challenge_updates["Strength Specialist"] = True

        # Challenge 4: Sports Enthusiast
        if sports_duration >= 300:  # 5 hours in minutes
            challenge_updates["Sports Enthusiast"] = True

        # Challenge 5: Calorie Crusher
        if total_calories >= 5000:
            challenge_updates["Calorie Crusher"] = True

        # Challenge 6: Fitness Variety
        if len(unique_exercises) >= 10:
            challenge_updates["Fitness Variety"] = True

        # Challenge 7: Coach's Pick
        if len(coach_count) >= 3:
            challenge_updates["Coach's Pick"] = True

        # Challenge 8: Long Haul
        if long_duration_workouts > 0:
            challenge_updates["Long Haul"] = True

        # Challenge 9: Workout Titan
        if total_workouts >= 30:
            challenge_updates["Workout Titan"] = True

        # Update challenges in Firestore
        for challenge_name, completed in challenge_updates.items():
            if completed:
                challenge_query = user_challenges_ref.where('challenge', '==', challenge_name).limit(1).stream()
                for challenge_doc in challenge_query:
                    challenge_doc.reference.update({'state': True})
        return True

    except Exception as e:
        print(f"Error updating workout challenges: {e}")
        return False