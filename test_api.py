import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:5000/api"


def test_register():
    """Test user registration"""
    url = f"{BASE_URL}/register"
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword",
    }

    response = requests.post(url, json=data)
    print(f"Register Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    print("---")

    return response.json()


def test_login():
    """Test user login"""
    url = f"{BASE_URL}/login"
    data = {"username": "testuser", "password": "securepassword"}

    response = requests.post(url, json=data)
    print(f"Login Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    print("---")

    return response.json().get("access_token")


def test_create_task(token):
    """Test creating a new task"""
    url = f"{BASE_URL}/tasks"
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task due tomorrow
    due_date = (datetime.now() + timedelta(days=1)).isoformat()

    data = {
        "title": "Test Task",
        "description": "This is a test task created by the test script",
        "priority": 2,
        "due_date": due_date,
    }

    response = requests.post(url, json=data, headers=headers)
    print(f"Create Task Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    print("---")

    return response.json().get("task", {}).get("id")


def test_get_tasks(token):
    """Test getting all tasks"""
    url = f"{BASE_URL}/tasks"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    print(f"Get Tasks Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    print("---")


def test_update_task(token, task_id):
    """Test updating a task"""
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}

    data = {"title": "Updated Test Task", "completed": True}

    response = requests.put(url, json=data, headers=headers)
    print(f"Update Task Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    print("---")


def test_delete_task(token, task_id):
    """Test deleting a task"""
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(url, headers=headers)
    print(f"Delete Task Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    print("---")


def run_tests():
    # Register a new user
    register_response = test_register()

    # Login with the new user
    token = test_login()
    if not token:
        print("Login failed, cannot continue tests")
        return

    # Create a new task
    task_id = test_create_task(token)
    if not task_id:
        print("Task creation failed, cannot continue tests")
        return

    # Get all tasks
    test_get_tasks(token)

    # Update the created task
    test_update_task(token, task_id)

    # Delete the task
    test_delete_task(token, task_id)


if __name__ == "__main__":
    print("Starting API Tests...")
    run_tests()
    print("Tests completed!")
