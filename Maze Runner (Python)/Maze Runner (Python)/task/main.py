import numpy as np
import random
import itertools


class Maze:
    space_symbol = "  "
    wall_symbol = "\u2588\u2588"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entrance_location = None
        self.exit_location = None
        self.must_be_paths = None
        self.maze_grid = self.generate_maze()

    def generate_maze(self):
        # Initialize maze grid with paths and borders
        maze_grid = np.full((self.height, self.width), 0)
        maze_grid[0, :] = 1
        maze_grid[:, 0] = 1
        maze_grid[self.height - 1, :] = 1
        maze_grid[:, self.width - 1] = 1
        # Randomly set exit and entrance, first find if entrance and exit will be along height or width
        ent_exit_factor = self.height
        if self.height > self.width:
            ent_exit_factor = self.width
        entrance_opening = random.choice(range(1, ent_exit_factor - 1))
        exit_opening = random.choice(range(1, ent_exit_factor - 1))
        if ent_exit_factor == self.height:
            self.entrance_location = (entrance_opening, 0)
            self.exit_location = (exit_opening, self.width - 1)
            self.must_be_paths = ([entrance_opening, exit_opening], [1, self.width - 2])
        else:
            self.entrance_location = (0, entrance_opening)
            self.exit_location = (self.height - 1, exit_opening)
            self.must_be_paths = ([0, self.height - 2], [entrance_opening, exit_opening])
        maze_grid[self.entrance_location] = 0
        maze_grid[self.exit_location] = 0

        return maze_grid

    def show_maze(self):
        # reference old maze grid, and make a new maze, fill in walls
        maze_grid = np.full((self.height, self.width), self.space_symbol)
        maze_grid[np.where(self.maze_grid == 1)] = self.wall_symbol
        maze_to_print = ""
        for row in maze_grid:
            maze_to_print += "".join(row)
            maze_to_print += "\n"
        print(maze_to_print)

    def generate_walls_empty_space(self):
        # create a 2 x 2 window
        # window_size = 2
        window_size = self.height - 2 if self.height < self.width else self.width - 2
        if self.height < 4 or self.width < 4:   # no windows possible if the maze is less than 4 x 4
            return
        while window_size > 1:
            for i in range(1, self.height - window_size):
                for j in range(1, self.width - window_size):
                    temp_window = self.maze_grid[i: i + window_size, j: j + window_size]
                    if not temp_window.any():  # if within window, there are no walls
                        rows = tuple(range(i, i + window_size))
                        cols = tuple(range(j, j + window_size))
                        temp_cells = list(itertools.product(rows, cols))  # grabs coordinates of all cells
                        temp_cells.sort()
                        to_remove = set()
                        for cell in temp_cells:  # removes any cells ineligible to be a wall
                            if not self.wall_eligibility(cell):
                                to_remove.add(cell)
                        rand_wall = list(set(temp_cells) - to_remove)
                        if rand_wall:  # randomly chooses a cell to be a wall within window, if there are any eligible
                            self.maze_grid[random.choice(rand_wall)] = 1
            window_size -= 1
            self.maze_grid[self.must_be_paths] = 0

    def generate_walls_empty_space_2(self):
        window_size = 2
        if self.height < 4 or self.width < 4:  # no windows possible if the maze is less than 4 x 4
            return
        last_maze = np.array([0])
        while not np.array_equal(last_maze, self.maze_grid):
            last_maze = self.maze_grid.copy()
            for i in range(1, self.height - window_size):
                for j in range(1, self.width - window_size):
                    temp_window = self.maze_grid[i: i + window_size, j: j + window_size]
                    if not temp_window.any():  # if within window, there are no walls
                        rows = tuple(range(i, i + window_size))
                        cols = tuple(range(j, j + window_size))
                        temp_cells = list(itertools.product(rows, cols))  # grabs coordinates of all cells
                        temp_cells.sort()
                        to_remove = set()
                        for cell in temp_cells:  # removes any cells ineligible to be a wall
                            if not self.wall_eligibility(cell):
                                to_remove.add(cell)
                        rand_wall = list(set(temp_cells) - to_remove)
                        if rand_wall:  # randomly chooses a cell to be a wall within window, if there are any eligible
                            self.maze_grid[random.choice(rand_wall)] = 1
            self.maze_grid[self.must_be_paths] = 0

    def generate_walls_empty_space_3(self):
        window_size = self.height - 2 if self.height < self.width else self.width - 2
        if self.height < 4 or self.width < 4:  # no windows possible if the maze is less than 4 x 4
            return
        while window_size > 1:
            last_maze = np.array([1])
            while not np.array_equal(last_maze, self.maze_grid):
                last_maze = self.maze_grid.copy()
                for i in range(1, self.height - window_size):
                    for j in range(1, self.width - window_size):
                        temp_window = self.maze_grid[i: i + window_size, j: j + window_size]
                        if not temp_window.any():  # if within window, there are no walls
                            rows = tuple(range(i, i + window_size))
                            cols = tuple(range(j, j + window_size))
                            temp_cells = list(itertools.product(rows, cols))  # grabs coordinates of all cells
                            temp_cells.sort()
                            to_remove = set()
                            for cell in temp_cells:  # removes any cells ineligible to be a wall
                                if not self.wall_eligibility(cell):
                                    to_remove.add(cell)
                            rand_wall = list(set(temp_cells) - to_remove)
                            if rand_wall:  # randomly chooses a cell to be a wall within window, if there are any eligible
                                self.maze_grid[random.choice(rand_wall)] = 1
                self.maze_grid[self.must_be_paths] = 0
            window_size -= 1

    # Create an eligibility check if a cell can be turned into a wall
    # Eligibility rule:
    # For all corners of the cell that has a wall, it must have a wall in a cardinal direction adjacent to both

    def wall_eligibility(self, cell_coord):
        # add a check that it must be next to a wall
        cluster_factor = 4
        row = cell_coord[0]
        col = cell_coord[1]
        wall_check = ([row, row, row + 1, row - 1], [col + 1, col - 1, col, col])
        if not self.maze_grid[wall_check].any():
            return False
        rows = (row - 1, row + 1)
        cols = (col - 1, col + 1)
        corners = list(itertools.product(rows, cols))  # creates combination of all corner coordinates around cell
        for corner in corners:
            if self.maze_grid[corner]:  # checks if the corner is a wall
                to_check = ([corner[0], row], [col, corner[1]])  # generates adjacent points
                if not self.maze_grid[to_check].any():  # if neither adjacent points are walls
                    return False  # this cell cannot be a wall
        # add a check for making sure 3 x 3 walls don't form
        low_row = row - 2
        high_row = row + 2
        low_col = col - 2
        high_col = col + 2
        window_size = 3
        for window_row in range(low_row, high_row + 1 - window_size):
            if window_row < 0 or window_row + 2 > self.height - 1:
                continue
            for window_col in range(low_col, high_col + 1 - window_size):
                if window_col < 0 or window_col > self.width - 1:
                    continue
                curr_window = self.maze_grid[window_row: window_row + 3, window_col: window_col + 3]
                if len(curr_window[curr_window == 0]) < cluster_factor:
                    return False
        return True


if __name__ == "__main__":
    width = 20
    height = 20
    my_maze = Maze(width, height)
    my_maze.generate_walls_empty_space_3()
    my_maze.show_maze()

# Need to implement a few algorithms
# Maze generator
# Constraints:
# - At least one block in a 3 x 3 square should be a pathway
# - There should only be two path blocks on the border of the maze that are on opposite sides
# - The width and height have to be at least 3 x 3
# - There should always be a path to the entrance or exit from any path i.e. all paths should connect
# 1. Create an m x n array of 1s on the borders to represent walls and 0s on the inside to represent paths
# 2. Randomly pick the entrance and exit along the shortest opposite sides and set them to 0
# 3. Moving 3 x 3 filter along the array to drop in zeros where there are none. At this point the
#    maze will look like a bunch of path patches
# 4.
