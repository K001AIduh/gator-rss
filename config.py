import os
from datetime import timedelta

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLite database file path
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'task_app.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret key for signing the JWT
SECRET_KEY = "your-secret-key-here"  # In production, use environment variables

# JWT configuration
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
