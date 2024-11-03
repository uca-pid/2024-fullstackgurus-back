from firebase_setup import db
from datetime import datetime

def add_water_intake_service(uid, quantity_in_militers, date, public=False):
    try:
        # Referencia al documento del usuario
        user_ref = db.collection('water_intakes').document(uid)
        user_doc = user_ref.get()

        # Si el documento no existe, lo creamos
        if not user_doc.exists:
            user_ref.set({})

        # Referencia a la subcolección de ingesta de agua del usuario
        water_intake_ref = user_ref.collection('user_water_intakes').document(date)

        # Verificar si ya hay una entrada para el día. Si existe, sumamos la cantidad.
        existing_water_intake = water_intake_ref.get()
        if existing_water_intake.exists:
            existing_data = existing_water_intake.to_dict()
            quantity_in_militers += existing_data.get('quantity_in_militers', 0)

        # Guardar o actualizar la ingesta de agua del día
        water_intake_ref.set({
            'quantity_in_militers': quantity_in_militers,
            'date': datetime.strptime(date, '%Y-%m-%d'), # Falta hacerle la correccion de gmt-3
            'public': public
        })

        return True

    except Exception as e:
        print(f"Error saving water intake: {e}")
        return False

def get_daily_water_intake_service(uid, date):
    try:
        # Referencia al documento de ingesta de agua del día
        water_intake_ref = db.collection('water_intakes').document(uid).collection('user_water_intakes').document(date)
        water_intake_doc = water_intake_ref.get()

        # Si no existe, retornamos 0
        if not water_intake_doc.exists:
            return None

        # Obtener la cantidad de mililitros
        water_intake_data = water_intake_doc.to_dict()
        return water_intake_data.get('quantity_in_militers', 0)

    except Exception as e:
        print(f"Error fetching daily water intake: {e}")
        return None

def get_water_intake_history_service(uid, start_date, end_date):
    try:
        # Referencia a la subcolección de ingesta de agua
        water_intake_ref = db.collection('water_intakes').document(uid).collection('user_water_intakes')

        # Filtrar por rango de fechas
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        water_intakes = water_intake_ref.where('date', '>=', start_datetime).where('date', '<=', end_datetime).stream()

        # Construir el historial
        history = []
        for intake in water_intakes:
            intake_data = intake.to_dict()
            history.append({
                'date': intake_data.get('date').strftime('%Y-%m-%d'),
                'quantity_in_militers': intake_data.get('quantity_in_militers', 0)
            })

        return history

    except Exception as e:
        print(f"Error fetching water intake history: {e}")
        return []
