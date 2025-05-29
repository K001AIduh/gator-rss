from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Task
from datetime import datetime

# Create blueprint for API routes
api = Blueprint("api", __name__, url_prefix="/api")


# User registration endpoint
@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Check if required fields are provided
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create new user
    new_user = User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify(
            {"message": "User registered successfully", "user": new_user.to_dict()}
        ),
        201,
    )


# User login endpoint
@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Check if required fields are provided
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    # Find user by username
    user = User.query.filter_by(username=data["username"]).first()

    # Check if user exists and password is correct
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create access token
    access_token = create_access_token(identity=user.id)

    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200


# Get all tasks for the current user
@api.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    # Get query parameters for filtering
    completed = request.args.get("completed")
    priority = request.args.get("priority")

    # Build query based on filters
    query = Task.query.filter_by(user_id=user_id)

    if completed is not None:
        completed_bool = completed.lower() == "true"
        query = query.filter_by(completed=completed_bool)

    if priority is not None:
        try:
            priority_int = int(priority)
            query = query.filter_by(priority=priority_int)
        except ValueError:
            pass

    # Execute query and convert results to dict
    tasks = query.all()
    result = [task.to_dict() for task in tasks]

    return jsonify({"tasks": result}), 200


# Create a new task
@api.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Check if required fields are provided
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Parse due date if provided
    due_date = None
    if "due_date" in data and data["due_date"]:
        try:
            due_date = datetime.fromisoformat(data["due_date"])
        except ValueError:
            return (
                jsonify(
                    {
                        "error": "Invalid date format for due_date. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                    }
                ),
                400,
            )

    # Create new task
    new_task = Task(
        title=data["title"],
        description=data.get("description", ""),
        completed=data.get("completed", False),
        due_date=due_date,
        priority=data.get("priority", 1),
        user_id=user_id,
    )

    db.session.add(new_task)
    db.session.commit()

    return (
        jsonify({"message": "Task created successfully", "task": new_task.to_dict()}),
        201,
    )


# Get, update, or delete a specific task
@api.route("/tasks/<int:task_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_task(task_id):
    user_id = get_jwt_identity()

    # Find task by ID and ensure it belongs to the current user
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return (
            jsonify(
                {"error": "Task not found or you don't have permission to access it"}
            ),
            404,
        )

    # GET request - Return the task
    if request.method == "GET":
        return jsonify({"task": task.to_dict()}), 200

    # PUT request - Update the task
    elif request.method == "PUT":
        data = request.get_json()

        # Update task fields if provided
        if "title" in data:
            task.title = data["title"]

        if "description" in data:
            task.description = data["description"]

        if "completed" in data:
            task.completed = data["completed"]

        if "priority" in data:
            task.priority = data["priority"]

        if "due_date" in data:
            if data["due_date"]:
                try:
                    task.due_date = datetime.fromisoformat(data["due_date"])
                except ValueError:
                    return (
                        jsonify(
                            {
                                "error": "Invalid date format for due_date. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                            }
                        ),
                        400,
                    )
            else:
                task.due_date = None

        db.session.commit()

        return (
            jsonify({"message": "Task updated successfully", "task": task.to_dict()}),
            200,
        )

    # DELETE request - Delete the task
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted successfully"}), 200
