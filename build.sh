#!/bin/bash

# Define the repository name - change this to your actual GitHub repo name
REPO_NAME="Boot.Dev"

# Build the site with the proper base path for GitHub Pages
python3 src/main.py "/$REPO_NAME/"

echo "Site built for GitHub Pages with base path: /$REPO_NAME/"
