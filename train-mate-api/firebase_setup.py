# firebase_setup.py
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase con tus credenciales
cred = credentials.Certificate("./trainmate-7ae2b-firebase-adminsdk-z5wai-314a13b3af.json")
firebase_admin.initialize_app(cred)

# Inicializar Firestore
db = firestore.client()