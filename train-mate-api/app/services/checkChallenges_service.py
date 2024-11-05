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