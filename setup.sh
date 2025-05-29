#!/bin/bash

# Exit on error
set -e

echo "Setting up Task Management API..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize the database
echo "Initializing database..."
python init_db.py

echo "Setup complete! You can now run the application with:"
echo "source venv/bin/activate"
echo "python app.py"
