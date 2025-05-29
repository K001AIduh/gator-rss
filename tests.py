import unittest
from maze_window import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_small(self):
        num_cols = 5
        num_rows = 3
        m = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        self.assertEqual(
            len(m._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m._Maze__cells[0]),
            num_rows,
        )

    def test_maze_large(self):
        num_cols = 50
        num_rows = 40
        m = Maze(0, 0, num_rows, num_cols, 5, 5, seed=0)
        self.assertEqual(
            len(m._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m._Maze__cells[0]),
            num_rows,
        )

    def test_maze_square(self):
        size = 15
        m = Maze(0, 0, size, size, 20, 20, seed=0)
        self.assertEqual(
            len(m._Maze__cells),
            size,
        )
        self.assertEqual(
            len(m._Maze__cells[0]),
            size,
        )

    def test_maze_different_cell_sizes(self):
        num_cols = 8
        num_rows = 6
        cell_size_x = 15
        cell_size_y = 25
        m = Maze(0, 0, num_rows, num_cols, cell_size_x, cell_size_y, seed=0)
        self.assertEqual(
            len(m._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m._Maze__cells[0]),
            num_rows,
        )

    def test_break_entrance_and_exit(self):
        num_cols = 10
        num_rows = 8
        m = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)

        # Check that entrance (top wall of top-left cell) is broken
        self.assertFalse(m._Maze__cells[0][0].has_top_wall)

        # Check that exit (bottom wall of bottom-right cell) is broken
        self.assertFalse(m._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall)

        # Check that some walls are still intact
        self.assertTrue(m._Maze__cells[0][0].has_left_wall)
        self.assertTrue(m._Maze__cells[num_cols - 1][num_rows - 1].has_right_wall)

    def test_all_cells_visited(self):
        num_cols = 5
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)

        # Set all cells to visited for testing
        for i in range(num_cols):
            for j in range(num_rows):
                m._Maze__cells[i][j].visited = True

        # Now reset them
        m._Maze__reset_cells_visited()

        # Check that all cells have been reset to not visited
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(m._Maze__cells[i][j].visited)

    def test_walls_broken(self):
        # Test with a fixed seed to ensure deterministic behavior
        m = Maze(0, 0, 3, 3, 10, 10, seed=42)

        # Count how many walls are broken in the maze
        broken_walls = 0
        for i in range(3):
            for j in range(3):
                if not m._Maze__cells[i][j].has_left_wall:
                    broken_walls += 1
                if not m._Maze__cells[i][j].has_right_wall:
                    broken_walls += 1
                if not m._Maze__cells[i][j].has_top_wall:
                    broken_walls += 1
                if not m._Maze__cells[i][j].has_bottom_wall:
                    broken_walls += 1

        # The number of broken walls should be greater than zero
        # and less than the total number of walls
        self.assertGreater(broken_walls, 0)

        # In a 3x3 maze with all walls, we would have 12 outer walls and 12 inner walls
        # Since we break the entrance and exit (2 walls) and break walls for the maze
        # generation, we expect some walls to be broken, but not all
        total_possible_walls = 24
        self.assertLess(broken_walls, total_possible_walls)

    def test_reset_cells_visited(self):
        # Create a maze
        num_cols = 4
        num_rows = 4
        m = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)

        # Set all cells to visited for testing
        for i in range(num_cols):
            for j in range(num_rows):
                m._Maze__cells[i][j].visited = True

        # Call the reset method
        m._Maze__reset_cells_visited()

        # Verify all cells are now marked as not visited
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(m._Maze__cells[i][j].visited)

    def test_maze_solving(self):
        # Create a small maze with a fixed seed to ensure deterministic behavior
        num_cols = 3
        num_rows = 3
        m = Maze(0, 0, num_rows, num_cols, 10, 10, seed=42)

        # Solve the maze
        result = m.solve()

        # The maze should be solvable
        self.assertTrue(result)

        # Check that the exit cell has been visited
        self.assertTrue(m._Maze__cells[num_cols - 1][num_rows - 1].visited)


if __name__ == "__main__":
    unittest.main()
