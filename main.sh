#!/bin/bash

# Run the main.py script from the src directory
python3 src/main.py

# Start a web server in the docs directory
cd docs && python3 -m http.server 8888
