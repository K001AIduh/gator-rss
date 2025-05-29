from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
import os


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Load the default configuration
    app.config.from_object("config")

    # Initialize database
    db.init_app(app)

    # Initialize JWT
    jwt = JWTManager(app)

    # Register blueprints
    from routes import api

    app.register_blueprint(api)

    # Create a simple index route
    @app.route("/")
    def index():
        return {
            "message": "Welcome to the Task Management API",
            "version": "1.0.0",
            "documentation": "/api",
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
