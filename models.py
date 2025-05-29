import sqlite3
import os
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "task_app.db")


def dict_factory(cursor, row):
    """Convert database row to dictionary"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_connection():
    """Create a database connection and return it"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    return conn


def init_db():
    """Initialize the database with tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    # Create tasks table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT 0,
        due_date TIMESTAMP,
        priority INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """
    )

    conn.commit()
    conn.close()


class User:
    @staticmethod
    def create(username, email, password):
        """Create a new user"""
        conn = get_db_connection()
        cursor = conn.cursor()

        password_hash = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash),
            )
            conn.commit()
            user_id = cursor.lastrowid
            user = User.get_by_id(user_id)
            return user
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """Get a user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        conn.close()
        return user

    @staticmethod
    def get_by_username(username):
        """Get a user by username"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        conn.close()
        return user

    @staticmethod
    def get_by_email(email):
        """Get a user by email"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        conn.close()
        return user

    @staticmethod
    def check_password(user, password):
        """Check if the password is correct for a user"""
        if not user:
            return False
        return check_password_hash(user["password_hash"], password)


class Task:
    @staticmethod
    def create(
        title, user_id, description=None, completed=False, due_date=None, priority=1
    ):
        """Create a new task"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Format due_date properly if provided
        if due_date:
            if isinstance(due_date, str):
                # Try to parse string to datetime
                due_date = datetime.fromisoformat(due_date)
            due_date = due_date.isoformat()

        cursor.execute(
            """INSERT INTO tasks
               (title, description, completed, due_date, priority, user_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (title, description, 1 if completed else 0, due_date, priority, user_id),
        )

        conn.commit()
        task_id = cursor.lastrowid
        task = Task.get_by_id(task_id, user_id)

        conn.close()
        return task

    @staticmethod
    def get_by_id(task_id, user_id):
        """Get a task by ID and ensure it belongs to the user"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)
        )
        task = cursor.fetchone()

        conn.close()
        return task

    @staticmethod
    def get_all_by_user(user_id, completed=None, priority=None):
        """Get all tasks for a user with optional filters"""
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM tasks WHERE user_id = ?"
        params = [user_id]

        if completed is not None:
            query += " AND completed = ?"
            params.append(1 if completed else 0)

        if priority is not None:
            query += " AND priority = ?"
            params.append(priority)

        query += " ORDER BY due_date ASC"

        cursor.execute(query, params)
        tasks = cursor.fetchall()

        conn.close()
        return tasks

    @staticmethod
    def update(task_id, user_id, **kwargs):
        """Update a task"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build update query dynamically based on provided fields
        allowed_fields = ["title", "description", "completed", "due_date", "priority"]
        update_parts = []
        params = []

        for field in allowed_fields:
            if field in kwargs:
                value = kwargs[field]

                # Special handling for completed (convert to integer)
                if field == "completed":
                    value = 1 if value else 0

                # Special handling for due_date
                if field == "due_date" and value:
                    if isinstance(value, str):
                        # Try to parse string to datetime
                        value = datetime.fromisoformat(value)
                    value = value.isoformat()

                update_parts.append(f"{field} = ?")
                params.append(value)

        # Add updated_at timestamp
        update_parts.append("updated_at = CURRENT_TIMESTAMP")

        if not update_parts:
            # No fields to update
            conn.close()
            return Task.get_by_id(task_id, user_id)

        # Complete the query
        query = (
            f"UPDATE tasks SET {', '.join(update_parts)} WHERE id = ? AND user_id = ?"
        )
        params.extend([task_id, user_id])

        cursor.execute(query, params)
        conn.commit()

        # Check if update was successful
        if cursor.rowcount == 0:
            conn.close()
            return None

        # Get the updated task
        task = Task.get_by_id(task_id, user_id)

        conn.close()
        return task

    @staticmethod
    def delete(task_id, user_id):
        """Delete a task"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)
        )
        conn.commit()

        # Check if deletion was successful
        success = cursor.rowcount > 0

        conn.close()
        return success
