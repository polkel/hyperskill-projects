import numpy as np
import random
import itertools


class Maze2:
    space_symbol = "  "
    wall_symbol = "\u2588\u2588"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entrance_cell = None
        self.exit_cell = None
        self.ends = set()
        self.grid = np.full((self.height, self.width), 1)  # initialize grid as all walls
        self.generate_maze()

    def generate_maze(self):
        start_row = random.choice(range(1, self.height - 1, 2))  # make sure not to start on a border
        start_col = random.choice(range(1, self.width - 1, 2))
        start_cell = (start_row, start_col)
        self.make_path(start_cell)

    def make_path(self, cell):
        self.grid[cell] = 0
        adjacent_cells = self.adjacent_cells(cell)
        for next_cell in adjacent_cells:
            if self.in_bounds(next_cell) and not self.grid[next_cell]:  # base case, cell is already open
                continue
            between_row = int((next_cell[0] + cell[0]) / 2)
            between_col = int((next_cell[1] + cell[1]) / 2)
            between_cell = (between_row, between_col)
            border = self.cell_border(next_cell)
            if border != "in":  # base case is that you hit a border
                if not self.entrance_cell:
                    if self.in_bounds(next_cell):
                        self.entrance_cell = next_cell
                    else:
                        self.entrance_cell = between_cell
                    self.grid[self.entrance_cell] = 0
                elif not self.exit_cell:
                    opposite = "up"
                    if border == "right":
                        opposite = "left"
                    elif border == "left":
                        opposite = "right"
                    elif border == "up":
                        opposite = "down"
                    if opposite == self.cell_border(self.entrance_cell):
                        if self.in_bounds(next_cell):
                            self.exit_cell = next_cell
                        else:
                            self.exit_cell = between_cell
                        self.grid[self.exit_cell] = 0
                else:
                    self.ends.add(cell)
                if self.cell_border(between_cell) == "in":
                    self.grid[between_cell] = 0
            else:
                self.grid[between_cell] = 0
                self.make_path(next_cell)

    @staticmethod
    def adjacent_cells(cell):
        cells = []
        row = cell[0]
        col = cell[1]
        row_above = row - 2
        row_below = row + 2
        col_left = col - 2
        col_right = col + 2
        cells.append((row, col_left))
        cells.append((row, col_right))
        cells.append((row_below, col))
        cells.append((row_above, col))
        random.shuffle(cells)
        return cells

    def cell_border(self, cell):  # Takes a cell coordinate and returns which side of the maze it's on
        row = cell[0]
        col = cell[1]
        left = col <= 0
        right = col >= self.width - 1
        up = row <= 0
        down = row >= self.height - 1
        result = "in"
        if left:
            result = "left"
        elif right:
            result = "right"
        elif up:
            result = "up"
        elif down:
            result = "down"
        return result

    def in_bounds(self, cell):
        row = cell[0]
        col = cell[1]
        up = row >= 0
        down = row <= self.height - 1
        left = col >= 0
        right = col <= self.width - 1
        return up and down and left and right

    def show_maze(self):
        # reference old maze grid, and make a new maze, fill in walls
        maze_grid = np.full((self.height, self.width), self.space_symbol)
        maze_grid[np.where(self.grid == 1)] = self.wall_symbol
        maze_to_print = ""
        for row in maze_grid:
            maze_to_print += "".join(row)
            maze_to_print += "\n"
        print(maze_to_print)


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
        # Every cell where the row and column index is even must be a wall tile (except for exit and entrance)
        # This will make the maze more maze like in quality
        # maze_grid[0: self.height - 1: 2, 0: self.width - 1: 2] = 1
        # Randomly set exit and entrance, first find if entrance and exit will be along height or width
        ent_exit_factor = self.height
        if self.height > self.width:
            ent_exit_factor = self.width
        entrance_opening = random.choice(range(1, ent_exit_factor - 1, 2))
        exit_opening = random.choice(range(1, ent_exit_factor - 1, 2))
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
                            temp_cells = set(itertools.product(rows, cols))  # grabs coordinates of all cells
                            to_remove = set()
                            for cell in temp_cells:  # removes any cells ineligible to be a wall
                                if not self.wall_eligibility(cell):
                                    to_remove.add(cell)
                            rand_wall = list(temp_cells - to_remove)
                            if rand_wall:  # randomly chooses a cell to be a wall within window, if there are any eligible
                                self.maze_grid[random.choice(rand_wall)] = 1
                self.maze_grid[self.must_be_paths] = 0
            window_size -= 1

    # Create an eligibility check if a cell can be turned into a wall
    # Eligibility rule:
    # For all corners of the cell that has a wall, it must have a wall in a cardinal direction adjacent to both

    def wall_eligibility(self, cell_coord):
        # this is what determines the maze like qualities of the algo
        # Need to implement that if the cell is in an even row or column, it must be a wall if it is adjacent to
        # another space in that even row or column
        # add a check that it must be next to a wall
        cluster_factor = 2
        row = cell_coord[0]
        col = cell_coord[1]
        if row % 2 == 1 and col % 2 == 1:
            return False
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
        if row % 2 == 0 and col % 2 == 0:
            self.maze_grid[(row, col)] = 1
            return False
        return True


if __name__ == "__main__":
    player_input = input("Please, enter the size of a maze\n")
    sizes = player_input.split(" ")
    width_input = int(sizes[1])
    height_input = int(sizes[0])
    my_maze = Maze2(width_input, height_input)
    # my_maze.generate_walls_empty_space_3()
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
# Ideas for a game:
# Collect power ups before the time runs out and exit the maze
# Use the time module and msvcrt, but maybe look into sys.stdin?

# Need to revise algorithm... every evenly indexed row and column cell need to be a wall
# Maybe we add the preference during the window check and remove the sort?
