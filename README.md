# Python Asteroids Game

A classic Asteroids arcade game built with Python and Pygame.

## Description

This is a clone of the classic Asteroids arcade game implemented in Python using the Pygame library. Control a spaceship and destroy asteroids while avoiding collisions.

## Features

- Player-controlled spaceship with rotation and thrust
- Asteroids that split into smaller ones when shot
- Collision detection
- Simple physics-based movement

## Controls

- W: Thrust forward
- A: Rotate left
- D: Rotate right
- S: Slow down / brake
- SPACE: Shoot

## Installation

1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the game:
   ```
   python main.py
   ```

## Requirements

- Python 3.x
- Pygame 2.6.1

## Game Mechanics

- Large asteroids split into medium ones when hit
- Medium asteroids split into small ones when hit
- Small asteroids disappear when hit
- Game ends when the player collides with an asteroid

## Future Enhancements

- Scoring system
- Multiple lives
- Sound effects
- Power-ups
- Screen wrapping
