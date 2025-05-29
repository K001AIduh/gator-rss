# Maze Generator and Solver

A Python application that generates and solves random mazes using depth-first search algorithms. The project uses Tkinter to visualize the maze generation and solving process.

## Features

- Generates random mazes using a depth-first search algorithm
- Solves mazes using a depth-first search algorithm
- Visualizes the maze generation and solving process
- Supports different maze sizes
- Includes animation for both generation and solving
- Uses optional seeding for reproducible mazes

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## How to Run

1. Clone this repository
2. Run the main script:
   ```
   python3 maze_window.py
   ```

## Project Structure

- `maze_window.py`: Main file containing the Window, Cell, and Maze classes
- `tests.py`: Unit tests for the maze generator and solver

## How It Works

1. The program creates a grid of cells, each with four walls.
2. The maze generation algorithm uses a depth-first search to break down walls between cells, creating a valid maze with exactly one path from the entrance to the exit.
3. The maze solving algorithm uses another depth-first search to find a path from the entrance (top-left) to the exit (bottom-right).
4. The process is animated, showing the exploration and solution paths.

## Future Improvements

Potential extensions to this project:

- Additional solving algorithms (BFS, A\*)
- User interface for configuring maze size and animation speed
- 3D maze generation and solving
- Interactive mode where users can navigate the maze
