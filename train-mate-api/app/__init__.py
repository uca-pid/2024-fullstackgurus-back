# app/__init__.py
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    @app.route('/')
    def home():
        return '¡Bienvenido a la API de TrainMate!'
    
    @app.route('/healthCheck')
    def check():
        return jsonify({
            'api': 'All is up working!'
        }), 200

    # Importar y registrar los blueprints (controladores)
    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from app.controllers.workout_controller import workout_bp
    app.register_blueprint(workout_bp)

    from app.controllers.excercise_controller import exercise_bp
    app.register_blueprint(exercise_bp, url_prefix='/api/exercise')

    return app