from flask import Flask, jsonify, request
import jwt
from datetime import datetime, timedelta
import os
from models import User, Task, init_db

# Secret key for JWT
SECRET_KEY = "your-secret-key-here"  # In production, use environment variables
# JWT expiration time
JWT_EXPIRATION = timedelta(hours=1)


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    # Ensure the database exists
    init_db()

    # Authentication helper functions
    def create_token(user_id):
        """Create a JWT token for a user"""
        payload = {
            "exp": datetime.utcnow() + JWT_EXPIRATION,
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def decode_token(token):
        """Decode a JWT token and return the user ID"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    def token_required(f):
        """Decorator for endpoints that require authentication"""

        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return (
                    jsonify({"error": "Missing or invalid authorization header"}),
                    401,
                )

            token = auth_header.split(" ")[1]
            user_id = decode_token(token)

            if not user_id:
                return jsonify({"error": "Invalid or expired token"}), 401

            return f(user_id, *args, **kwargs)

        # Preserve the function name and docstring
        decorated.__name__ = f.__name__
        decorated.__doc__ = f.__doc__

        return decorated

    # API Routes

    # User registration endpoint
    @app.route("/api/register", methods=["POST"])
    def register():
        data = request.get_json()

        # Check if required fields are provided
        required_fields = ["username", "email", "password"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Check if username or email already exists
        if User.get_by_username(data["username"]):
            return jsonify({"error": "Username already exists"}), 400

        if User.get_by_email(data["email"]):
            return jsonify({"error": "Email already exists"}), 400

        # Create new user
        user = User.create(
            username=data["username"], email=data["email"], password=data["password"]
        )

        if not user:
            return jsonify({"error": "Failed to create user"}), 500

        # Don't return the password hash
        user.pop("password_hash", None)

        return jsonify({"message": "User registered successfully", "user": user}), 201

    # User login endpoint
    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json()

        # Check if required fields are provided
        if "username" not in data or "password" not in data:
            return jsonify({"error": "Username and password are required"}), 400

        # Find user by username
        user = User.get_by_username(data["username"])

        # Check if user exists and password is correct
        if not user or not User.check_password(user, data["password"]):
            return jsonify({"error": "Invalid username or password"}), 401

        # Create access token
        access_token = create_token(user["id"])

        # Don't return the password hash
        user.pop("password_hash", None)

        return jsonify({"access_token": access_token, "user": user}), 200

    # Get all tasks for the current user
    @app.route("/api/tasks", methods=["GET"])
    @token_required
    def get_tasks(user_id):
        # Get query parameters for filtering
        completed_param = request.args.get("completed")
        priority_param = request.args.get("priority")

        # Convert parameters to appropriate types
        completed = None
        if completed_param is not None:
            completed = completed_param.lower() == "true"

        priority = None
        if priority_param is not None:
            try:
                priority = int(priority_param)
            except ValueError:
                pass

        # Get tasks with filters
        tasks = Task.get_all_by_user(user_id, completed, priority)

        return jsonify({"tasks": tasks}), 200

    # Create a new task
    @app.route("/api/tasks", methods=["POST"])
    @token_required
    def create_task(user_id):
        data = request.get_json()

        # Check if required fields are provided
        if "title" not in data:
            return jsonify({"error": "Title is required"}), 400

        # Create new task
        task = Task.create(
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            due_date=data.get("due_date"),
            priority=data.get("priority", 1),
            user_id=user_id,
        )

        if not task:
            return jsonify({"error": "Failed to create task"}), 500

        return jsonify({"message": "Task created successfully", "task": task}), 201

    # Get, update, or delete a specific task
    @app.route("/api/tasks/<int:task_id>", methods=["GET", "PUT", "DELETE"])
    @token_required
    def manage_task(user_id, task_id):
        # GET request - Return the task
        if request.method == "GET":
            task = Task.get_by_id(task_id, user_id)

            if not task:
                return (
                    jsonify(
                        {
                            "error": "Task not found or you don't have permission to access it"
                        }
                    ),
                    404,
                )

            return jsonify({"task": task}), 200

        # PUT request - Update the task
        elif request.method == "PUT":
            data = request.get_json()

            # Update fields
            task = Task.update(
                task_id=task_id,
                user_id=user_id,
                title=data.get("title"),
                description=data.get("description"),
                completed=data.get("completed"),
                due_date=data.get("due_date"),
                priority=data.get("priority"),
            )

            if not task:
                return (
                    jsonify(
                        {
                            "error": "Task not found or you don't have permission to access it"
                        }
                    ),
                    404,
                )

            return jsonify({"message": "Task updated successfully", "task": task}), 200

        # DELETE request - Delete the task
        elif request.method == "DELETE":
            success = Task.delete(task_id, user_id)

            if not success:
                return (
                    jsonify(
                        {
                            "error": "Task not found or you don't have permission to access it"
                        }
                    ),
                    404,
                )

            return jsonify({"message": "Task deleted successfully"}), 200

    # Create a simple index route
    @app.route("/")
    def index():
        return jsonify(
            {
                "message": "Welcome to the Task Management API",
                "version": "1.0.0",
                "documentation": "/api",
            }
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
