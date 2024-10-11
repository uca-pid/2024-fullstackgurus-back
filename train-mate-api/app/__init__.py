# app/__init__.py
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,  # Usar la IP del cliente como clave
    default_limits=["2 per second"]  # Límite por defecto
)


def create_app():
    app = Flask(__name__)
    #limiter.init_app(app)
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

    from app.controllers.categoy_controller import category_bp
    app.register_blueprint(category_bp, url_prefix='/api/category')

    from app.controllers.trainings_controller import trainings_bp
    app.register_blueprint(trainings_bp, url_prefix='/api/trainings')

    return app
