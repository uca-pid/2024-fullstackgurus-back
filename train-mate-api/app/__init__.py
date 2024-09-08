# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importar y registrar los blueprints (controladores)
    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from app.controllers.workout_controller import workout_bp
    app.register_blueprint(workout_bp)

    return app
