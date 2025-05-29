from app import create_app
from models import db

# Create an application instance with the app factory
app = create_app()

# Push an application context to make the app aware of the db
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")
