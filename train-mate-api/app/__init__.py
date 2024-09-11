# app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Permitir CORS desde cualquier origen
    CORS(app)

    # O para permitir específicamente solicitudes desde 'http://localhost:3000':
    # CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    @app.route('/')
    def home():
        return '¡Bienvenido a la API de TrainMate!'

    # Importar y registrar los blueprints (controladores)
    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from app.controllers.workout_controller import workout_bp
    app.register_blueprint(workout_bp)

    return app