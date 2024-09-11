import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Try to load environment variables from a .env file (for local development)
from dotenv import load_dotenv

# Load .env only if it exists (safe for Render which does not use .env)
load_dotenv()

# Load Firebase credentials from environment variable
firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS')

if firebase_creds_json:
    # Parse the JSON string (from the environment variable)
    firebase_creds_dict = json.loads(firebase_creds_json)

    # Initialize Firebase with the credentials loaded from environment variables
    cred = credentials.Certificate(firebase_creds_dict)
    firebase_admin.initialize_app(cred)

    # Initialize Firestore
    db = firestore.client()
else:
    raise Exception("FIREBASE_CREDENTIALS environment variable not set.")
