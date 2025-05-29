from tkinter import Tk, BOTH, Canvas
import time
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2,
        )


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.__win is None:
            return

        # Draw the left wall
        line = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
        self.__win.draw_line(line, "black" if self.has_left_wall else "#d9d9d9")

        # Draw the top wall
        line = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
        self.__win.draw_line(line, "black" if self.has_top_wall else "#d9d9d9")

        # Draw the right wall
        line = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
        self.__win.draw_line(line, "black" if self.has_right_wall else "#d9d9d9")

        # Draw the bottom wall
        line = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
        self.__win.draw_line(line, "black" if self.has_bottom_wall else "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return

        # Calculate the center of the current cell
        x_mid = (self.__x1 + self.__x2) // 2
        y_mid = (self.__y1 + self.__y2) // 2

        # Calculate the center of the destination cell
        to_x_mid = (to_cell.__x1 + to_cell.__x2) // 2
        to_y_mid = (to_cell.__y1 + to_cell.__y2) // 2

        # Set the color based on the undo flag
        color = "gray" if undo else "red"

        # Draw a line from the center of this cell to the center of the destination cell
        line = Line(Point(x_mid, y_mid), Point(to_x_mid, to_y_mid))
        self.__win.draw_line(line, color)


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Generator")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []

        # Set the random seed if provided
        if seed is not None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)  # Start breaking walls from the top-left cell
        self.__reset_cells_visited()  # Reset visited flags after breaking walls

    def __create_cells(self):
        # Initialize the grid of cells
        for i in range(self.__num_cols):
            column = []
            for j in range(self.__num_rows):
                cell = Cell(self.__win)
                column.append(cell)
            self.__cells.append(column)

        # Draw each cell at its position
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        # Calculate the position of the cell
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y

        # Draw the cell
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        # Break the entrance (top wall of the top-left cell)
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)

        # Break the exit (bottom wall of the bottom-right cell)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        # Mark the current cell as visited
        self.__cells[i][j].visited = True

        while True:
            # Create a list to hold possible directions
            possible_directions = []

            # Check all four adjacent cells
            # Check left
            if i > 0 and not self.__cells[i - 1][j].visited:
                possible_directions.append((i - 1, j, "left"))

            # Check right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                possible_directions.append((i + 1, j, "right"))

            # Check up
            if j > 0 and not self.__cells[i][j - 1].visited:
                possible_directions.append((i, j - 1, "up"))

            # Check down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                possible_directions.append((i, j + 1, "down"))

            # If there are no possible directions, draw the cell and return
            if len(possible_directions) == 0:
                self.__draw_cell(i, j)
                return

            # Choose a random direction
            direction_index = random.randrange(len(possible_directions))
            next_i, next_j, direction = possible_directions[direction_index]

            # Break down the walls between current cell and chosen cell
            if direction == "left":
                self.__cells[i][j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
            elif direction == "right":
                self.__cells[i][j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            elif direction == "up":
                self.__cells[i][j].has_top_wall = False
                self.__cells[next_i][next_j].has_bottom_wall = False
            elif direction == "down":
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False

            # Recursively visit the chosen cell
            self.__break_walls_r(next_i, next_j)

    def __reset_cells_visited(self):
        # Reset the visited property of all cells to False
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j].visited = False

    def solve(self):
        """
        Solve the maze using depth-first search.
        Returns True if a path was found, False otherwise.
        """
        # Reset all cells' visited flags before solving
        self.__reset_cells_visited()
        # Start solving from the entrance (top-left cell)
        return self.__solve_r(0, 0)

    def __solve_r(self, i, j):
        """
        Recursive helper method to solve the maze using depth-first search.
        Returns True if this cell is or leads to the exit, False otherwise.
        """
        # Animate the exploration
        self.__animate()

        # Mark the current cell as visited
        self.__cells[i][j].visited = True

        # If we've reached the end cell (bottom-right), we've solved the maze
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        # Check all four directions (left, right, up, down)
        # Left
        if (
            i > 0
            and not self.__cells[i][j].has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            # Draw a move to the left cell
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            # Recursively try to solve from the left cell
            if self.__solve_r(i - 1, j):
                return True
            # If that didn't work, undo the move
            self.__cells[i][j].draw_move(self.__cells[i - 1][j], True)

        # Right
        if (
            i < self.__num_cols - 1
            and not self.__cells[i][j].has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            # Draw a move to the right cell
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            # Recursively try to solve from the right cell
            if self.__solve_r(i + 1, j):
                return True
            # If that didn't work, undo the move
            self.__cells[i][j].draw_move(self.__cells[i + 1][j], True)

        # Up
        if (
            j > 0
            and not self.__cells[i][j].has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            # Draw a move to the upper cell
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            # Recursively try to solve from the upper cell
            if self.__solve_r(i, j - 1):
                return True
            # If that didn't work, undo the move
            self.__cells[i][j].draw_move(self.__cells[i][j - 1], True)

        # Down
        if (
            j < self.__num_rows - 1
            and not self.__cells[i][j].has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            # Draw a move to the lower cell
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            # Recursively try to solve from the lower cell
            if self.__solve_r(i, j + 1):
                return True
            # If that didn't work, undo the move
            self.__cells[i][j].draw_move(self.__cells[i][j + 1], True)

        # If none of the directions worked, this path is a dead end
        return False


def main():
    win = Window(800, 600)

    # Create a small 3x3 maze with a fixed seed
    small_maze = Maze(50, 50, 3, 3, 50, 50, win, 1)
    print("Solving small maze...")
    if small_maze.solve():
        print("Small maze solved!")
    else:
        print("Small maze could not be solved!")

    # Create a larger maze with a different seed
    large_maze = Maze(250, 50, 10, 15, 20, 20, win, 2)
    print("Solving large maze...")
    if large_maze.solve():
        print("Large maze solved!")
    else:
        print("Large maze could not be solved!")

    win.wait_for_close()


if __name__ == "__main__":
    main()
