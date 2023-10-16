import numpy as np
import math


class Game:
    def __init__(self):
        self.grid = None
        self.current_piece = None

    def new_game(self):
        grid_sizes = input().split()
        width = int(grid_sizes[0])  # TODO grid size validation (not less than 4)
        height = int(grid_sizes[1])
        self.grid = Grid(width, height)
        self.grid.show_grid()
        self.game_input()

    def add_piece(self, shape, top_left):
        self.current_piece = Piece(shape, top_left)  # TODO check if piece can be added to grid, otherwise game over

    def game_input(self):  # main workflow of every turn, can probably be broken up further
        player_input = input()
        while player_input != "exit":
            if self.current_piece:
                self.current_piece.down()
                if self.piece_out_of_bounds() or self.piece_collision():
                    self.current_piece.revert_location()
                    self.current_piece.can_move = False
                    # Check for game over according to the project
                    game_over = len(np.where(self.current_piece.location[0] == 0)[0]) > 0
                    if game_over:
                        self.grid.show_grid(self.current_piece)
                        print("Game Over!")
                        break
                    self.commit_piece()

            if self.current_piece:
                self.current_piece.last_location = self.current_piece.location.copy()
                if player_input == "left":
                    self.current_piece.left()
                    if self.piece_out_of_bounds() or self.piece_collision():
                        self.current_piece.revert_location()
                elif player_input == "right":
                    self.current_piece.right()
                    if self.piece_out_of_bounds() or self.piece_collision():
                        self.current_piece.revert_location()
                elif player_input == "rotate":
                    self.current_piece.rotate()
                    if self.piece_out_of_bounds() or self.piece_collision():
                        self.adjust_piece()
                self.current_piece.last_location = self.current_piece.location.copy()  # copies last legal location
                # self.current_piece.down()  # Down option happens by default in this implementation
                # if self.piece_out_of_bounds() or self.piece_collision():
                #     self.current_piece.revert_location()
                #     self.current_piece.can_move = False
                # self.current_piece.last_location = self.current_piece.location.copy()
                # TODO commit old piece to grid and trigger new piece to be added

            if player_input == "piece":
                shape = input()  # TODO piece validation
                self.add_piece(shape, self.grid.piece_start)

            if player_input == "break":
                rows_to_break = []
                rows_to_add = 0
                for row in range(len(self.grid.grid)):
                    if (self.grid.grid[row, ...] == "0").all():
                        rows_to_break.append(row)
                        rows_to_add += 1

                # while len(rows_to_break) > 0:
                #     row_to_break = rows_to_break.pop()
                self.grid.grid = np.delete(self.grid.grid, rows_to_break, axis=0)
                self.grid.grid = np.insert(self.grid.grid, 0, np.full((rows_to_add, self.grid.width), "-"), axis=0)

            self.grid.show_grid(self.current_piece)
            player_input = input()

    def piece_out_of_bounds(self):
        height_out_of_bounds = len(np.where(self.current_piece.location[0] >= self.grid.height)[0]) > 0
        left_out_of_bounds = len(np.where(self.current_piece.location[1] < 0)[0]) > 0
        right_out_of_bounds = len(np.where(self.current_piece.location[1] >= self.grid.width)[0]) > 0
        return height_out_of_bounds or left_out_of_bounds or right_out_of_bounds

    def piece_collision(self):
        spaces_in_location = self.grid.grid[*self.current_piece.location]
        collision = len(np.where(spaces_in_location == "0")[0]) > 0
        return collision

    def adjust_piece(self):  # checks if adjusting after the rotation of a piece is a legal move
        adjustments = self.current_piece.adjustments[self.current_piece.rotation_state].copy()
        while len(adjustments) > 0:
            adjustment = adjustments.pop()
            if adjustment == "up":
                self.current_piece.up()
            elif adjustment == "left":
                self.current_piece.left()
            elif adjustment == "right":
                self.current_piece.right()
            elif adjustment == "down":
                self.current_piece.down()
            if not (self.piece_out_of_bounds() or self.piece_collision()):
                return True
        self.current_piece.rotation_state = (self.current_piece.rotation_state - 1) % len(self.current_piece.rotations)
        self.current_piece.revert_location()
        return False

    def commit_piece(self):
        self.grid.grid[*self.current_piece.location] = "0"
        self.current_piece = None


class Grid:
    PIECE_SYMBOL = "0"
    EMPTY_SYMBOL = "-"

    def __init__(self, width, height):
        self.piece_start = np.array([[0], [math.floor(width/2) - 2]])  # TODO calculate top left coord for piece start
        self.width = width
        self.height = height
        self.grid = np.full((height, width), "-")

    def show_grid(self, piece=None):
        grid_to_print = self.grid.copy()
        if piece:
            grid_to_print[*piece.location] = "0"
        array_str = np.array2string(grid_to_print)
        grid_str = array_str.replace("[", "").replace("]", "").replace("'", "").replace("\n ", "\n")
        print(grid_str)
        print()

    def commit_piece(self, piece):
        pass

    def clear_lines(self):
        pass


class Piece:

    """
    Explain how piece dictionaries work and grid system
    """
    pieces = dict()
    rotations_dict = dict()
    adjustments_dict = dict()

    pieces["O"] = np.array([[0, 0, 1, 1], [1, 2, 1, 2]])
    rotations_dict["O"] = [np.array([[0, 0, 0, 0], [0, 0, 0, 0]])]
    adjustments_dict["O"] = [[]]

    pieces["I"] = np.array([[0, 1, 2, 3], [1, 1, 1, 1]])
    rotations_dict["I"] = [np.array([[0, 1, 2, 3], [1, 0, -1, -2]]),
                      np.array([[0, -1, -2, -3], [-1, 0, 1, 2]])]
    adjustments_dict["I"] = [["up", "up", "up"],
                        ["left", "left", "left", "right"]]

    pieces["S"] = np.array([[0, 0, 1, 1], [1, 2, 0, 1]])
    rotations_dict["S"] = [np.array([[-1, 0, -1, 0], [0, 1, -2, -1]]),
                      np.array([[1, 0, 1, 0], [0, -1, 2, 1]])]
    adjustments_dict["S"] = [["right"],
                        ["up"]]

    pieces["Z"] = np.array([[0, 0, 1, 1], [1, 2, 2, 3]])
    rotations_dict["Z"] = [np.array([[0, -1, 0, -1], [-1, 0, 1, 2]]),
                      np.array([[0, 1, 0, 1], [1, 0, -1, -2]])]
    adjustments_dict["Z"] = [["left"],
                        ["up"]]

    pieces["L"] = np.array([[0, 1, 2, 2], [1, 1, 1, 2]])
    rotations_dict["L"] = [np.array([[0, 1, 2, 1], [-2, -1, 0, 1]]),
                      np.array([[1, 0, -1, -2], [-1, 0, 1, 0]]),
                      np.array([[1, 0, -1, 0], [2, 1, 0, -1]]),
                      np.array([[-2, -1, 0, 1], [1, 0, -1, 0]])]
    adjustments_dict["L"] = [["up"],
                        ["right"],
                        ["up"],
                        ["left"]]

    pieces["J"] = np.array([[0, 1, 2, 2], [2, 2, 2, 1]])
    rotations_dict["J"] = [np.array([[-1, 0, 1, 2], [-1, 0, 1, 0]]),
                      np.array([[0, -1, -2, -1], [-2, -1, 0, 1]]),
                      np.array([[2, 1, 0, -1], [1, 0, -1, 0]]),
                      np.array([[-1, 0, 1, 0], [2, 1, 0, -1]])]
    adjustments_dict["J"] = [["up"],
                        ["right"],
                        ["down"],
                        ["left"]]

    pieces["T"] = np.array([[0, 1, 1, 2], [1, 1, 2, 1]])
    rotations_dict["T"] = [np.array([[0, 1, 0, 2], [-2, -1, 0, 0]]),
                      np.array([[1, 0, -1, -1], [-1, 0, -1, 1]]),
                      np.array([[1, 0, 1, -1], [2, 1, 0, 0]]),
                      np.array([[-2, -1, 0, 0], [1, 0, 1, -1]])]
    adjustments_dict["T"] = [["up"],
                        ["right"],
                        ["up"],
                        ["left"]]

    #     O:
    #
    #     - 0 0 -
    #     - 0 0 -
    #     - - - -
    #     - - - -
    #
    #     I:
    #
    #     - 0 - -   0 0 0 0
    #     - 0 - -   - - - -
    #     - 0 - -   - - - -
    #     - 0 - -   - - - -
    #
    #     S:
    #
    #     - 0 0 -   - 0 - -
    #     0 0 - -   - 0 0 -
    #     - - - -   - - 0 -
    #     - - - -   - - - -
    #
    #     Z:
    #
    #     - 0 0 -   - - 0 -
    #     - - 0 0   - 0 0 -
    #     - - - -   - 0 - -
    #     - - - -   - - - -
    #
    #     L:
    #
    #     - 0 - -   - - 0 -   - 0 0 -   - 0 0 0
    #     - 0 - -   0 0 0 -   - - 0 -   - 0 - -
    #     - 0 0 -   - - - -   - - 0 -   - - - -
    #     - - - -   - - - -   - - - -   - - - -
    #
    #     J:
    #
    #     - - 0 -   0 0 0 -   - 0 0 -   - 0 - -
    #     - - 0 -   - - 0 -   - 0 - -   - 0 0 0
    #     - 0 0 -   - - - -   - 0 - -   - - - -
    #     - - - -   - - - -   - - - -   - - - -
    #
    #     T:
    #
    #     - 0 - -   - 0 - -   - - 0 -   - 0 0 0
    #     - 0 0 -   0 0 0 -   - 0 0 -   - - 0 -
    #     - 0 - -   - - - -   - - 0 -   - - - -
    #     - - - -   - - - -   - - - -   - - - -

    def __init__(self, shape, top_left_start):
        self.shape = shape
        self.location = self.pieces[shape].copy() + top_left_start  # first array is row, second array is column
        self.last_location = self.location.copy()
        self.rotations = self.rotations_dict[shape]
        self.rotation_state = 0
        self.adjustments = self.adjustments_dict[shape]  # This will be related to current rotation state
        self.can_move = True

    def up(self):
        self.location[0, ...] -= 1

    def down(self):
        self.location[0, ...] += 1

    def left(self):
        self.location[1, ...] -= 1

    def right(self):
        self.location[1, ...] += 1

    def rotate(self):
        self.rotation_state = (self.rotation_state + 1) % len(self.rotations)
        self.location = self.location + self.rotations[self.rotation_state]

    def revert_location(self):
        self.location = self.last_location.copy()


if __name__ == "__main__":
    game = Game()
    game.new_game()

# TODO Automate block breaking and piece creation (maybe during commit_piece)
# TODO Double check actual game flow
# TODO Keep track of score
# TODO Use pytimedinput to make it timed, do these outside of Hyperskill


# # Refactor!
# class Grid:
#     def __init__(self, dimensions):
#         self.dimensions = dimensions
#         dimensions_split = self.dimensions.split()
#         self.width = int(dimensions_split[0])  # need to make checks later this is at least 4
#         self.height = int(dimensions_split[1])
#         self.game_grid = self.create_game_grid()
#         self.index_grid = self.create_index_grid()
#         self.piece_start_ind = math.floor(self.width / 2) - 2
#         self.temp_grid = None
#         self.curr_piece = None
#
#     def create_game_grid(self):
#         return np.full((self.height, self.width), "-")
#
#     def create_index_grid(self):
#         return np.arange(self.width * self.height).reshape(self.height, self.width)
#
#     def grid_to_str(self, grid_to_print=None):
#         if grid_to_print is None:
#             grid_to_print = self.game_grid
#         array_str = np.array2string(grid_to_print)
#         grid_str = array_str.replace("[", "").replace("]", "").replace("'", "").replace("\n ", "\n")
#         return grid_str
#
#     def add_curr_piece(self, curr_piece):
#         self.curr_piece = curr_piece
#         self.refresh_temp_grid()
#
#     def refresh_temp_grid(self):
#         piece_indices = self.curr_piece.get_piece_locations()
#         grid_copy = self.game_grid.copy()
#         grid_copy.put(piece_indices, "0")
#         self.temp_grid = grid_copy
#         # self.can_piece_move(piece_indices)
#
#     # def can_piece_move(self, piece_indices):
#     #     next_locations = piece_indices + self.width
#     #     out_of_bounds = np.where(next_locations >= self.width * self.height)
#     #     if len(out_of_bounds[0]) > 0:
#     #         self.curr_piece.can_move = False
#     #         return
#     #     piece_collision = np.where(self.game_grid.flat[next_locations] == "0")
#     #     if len(piece_collision[0]) > 0:
#     #         self.curr_piece.can_move = False
#
#
# class Piece:
#
#     """
#     This class represents each piece instance as they are added onto the game grid.
#
#     Each instance of this class is dependent on a Grid object already being created.
#     This piece instance will store its location indices according to the grid's dimensions.
#
#     The piece_dict below stores all the rotations of the possible pieces in a 4 x 4 grid.
#     Below is a figure showing how the 4 x 4 grid is indexed.
#
#     00 01 02 03
#     04 05 06 07
#     08 09 10 11
#     12 13 14 15
#
#     Here are the piece representations for all rotations
#     O:
#
#     - 0 0 -
#     - 0 0 -
#     - - - -
#     - - - -
#
#     I:
#
#     - 0 - -   0 0 0 0
#     - 0 - -   - - - -
#     - 0 - -   - - - -
#     - 0 - -   - - - -
#
#     S:
#
#     - 0 0 -   - 0 - -
#     0 0 - -   - 0 0 -
#     - - - -   - - 0 -
#     - - - -   - - - -
#
#     Z:
#
#     - 0 0 -   - - 0 -
#     - - 0 0   - 0 0 -
#     - - - -   - 0 - -
#     - - - -   - - - -
#
#     L:
#
#     - 0 - -   - - 0 -   - 0 0 -   - 0 0 0
#     - 0 - -   0 0 0 -   - - 0 -   - 0 - -
#     - 0 0 -   - - - -   - - 0 -   - - - -
#     - - - -   - - - -   - - - -   - - - -
#
#     J:
#
#     - - 0 -   0 0 0 -   - 0 0 -   - 0 - -
#     - - 0 -   - - 0 -   - 0 - -   - 0 0 0
#     - 0 0 -   - - - -   - 0 - -   - - - -
#     - - - -   - - - -   - - - -   - - - -
#
#     T:
#
#     - 0 - -   - 0 - -   - - 0 -   - 0 0 0
#     - 0 0 -   0 0 0 -   - 0 0 -   - - 0 -
#     - 0 - -   - - - -   - - 0 -   - - - -
#     - - - -   - - - -   - - - -   - - - -
#     """
#
#     piece_dict = dict()
#     piece_dict["O"] = [[1, 2, 5, 6]]
#     piece_dict["I"] = [[1, 5, 9, 13], [0, 1, 2, 3]]
#     piece_dict["S"] = [[2, 1, 5, 4], [1, 5, 6, 10]]
#     piece_dict["Z"] = [[1, 2, 6, 7], [2, 5, 6, 9]]
#     piece_dict["L"] = [[1, 5, 9, 10], [2, 4, 5, 6], [1, 2, 6, 10], [1, 2, 3, 5]]
#     piece_dict["J"] = [[2, 6, 9, 10], [0, 1, 2, 6], [1, 2, 5, 9], [1, 5, 6, 7]]
#     piece_dict["T"] = [[1, 5, 6, 9], [1, 4, 5, 6], [2, 5, 6, 10], [1, 2, 3, 6]]
#
#     def __init__(self, piece_shape, grid):
#         self.piece_input = piece_shape
#         self.piece_rotations = self.piece_dict[piece_input]  # must validate later
#         self.curr_rotation = 0  # can be randomized later for piece variation
#         self.grid = grid
#         self.location = self.create_start_location()
#         self.piece_grid = self.create_piece_array()
#         self.can_move = True
#
#     def create_start_location(self):
#         start_location = np.arange(16).reshape(4, 4)
#         start_location = start_location + self.grid.piece_start_ind
#         for i in range(1, 4):
#             start_location[i, ...] = start_location[i, ...] + i * (self.grid.width - 4)
#         return start_location
#
#     def create_piece_array(self):
#         piece_grid = np.full((4, 4), "-")
#         piece_grid.put(self.piece_rotations[self.curr_rotation], "0")
#         return piece_grid
#
#     def rotate(self):
#         if self.can_move:
#             self.curr_rotation = (self.curr_rotation + 1) % len(self.piece_rotations)
#             self.piece_grid = self.create_piece_array()
#             self.move_down()
#
#     def move_down(self):
#         if self.can_move:
#             self.location = self.location + self.grid.width
#
#     def move_left(self, override=False):
#         if self.can_move and self.check_left_possible() or override:
#             for i in range(4):
#                 column_to_change = self.location[..., i]
#                 add_width_check = (column_to_change[0] % self.grid.width) - 1
#                 column_to_change = column_to_change - 1
#                 if add_width_check == -1:  # handles side overflow
#                     column_to_change = column_to_change + self.grid.width
#                 self.location[..., i] = column_to_change
#         self.move_down()
#
#     def move_right(self, override=False):  # like move_left but checks the other way. can probably be condensed later
#         if self.can_move and self.check_right_possible() or override:
#             for i in range(4):
#                 column_to_change = self.location[..., i]
#                 sub_width_check = (column_to_change[0] % self.grid.width) + 1
#                 column_to_change = column_to_change + 1
#                 if sub_width_check == self.grid.width:  # handles side overflow
#                     column_to_change = column_to_change - self.grid.width
#                 self.location[..., i] = column_to_change
#         self.move_down()
#
#     def get_piece_locations(self):
#         piece_rows, piece_cols = np.where(self.piece_grid == "0")
#         piece_indices = piece.location[piece_rows, piece_cols]
#         # piece_indices = []
#         # for i in range(len(piece_rows)):
#         #     row = piece_rows[i]
#         #     col = piece_cols[i]
#         #     piece_indices.append(piece.location[row, col])
#         return piece_indices  # returns the single dimensional index of each pixel of the piece
#
#     def check_left_possible(self):  # still need to implement check for pieces
#         piece_indices = self.get_piece_locations()
#         for piece_index in piece_indices:
#             if piece_index % self.grid.width == 0:  # checks for wall
#                 return False
#         if self.check_for_pieces("left", piece_indices):
#             return False
#         return True
#
#     def check_right_possible(self):
#         piece_indices = self.get_piece_locations()
#         for piece_index in piece_indices:
#             if (piece_index + 1) % self.grid.width == 0:  # check for wall
#                 return False
#         if self.check_for_pieces("right", piece_indices):  # checks if an existing piece is in new spots
#             return False
#         return True
#
#     def check_for_pieces(self, direction, curr_locations):
#         new_space = 0
#         if direction == "right":
#             new_space = 1
#         else:
#             new_space = -1
#         next_location = curr_locations + new_space
#         next_location_on_grid = self.grid.game_grid.flat[next_location]
#         if len(np.where(next_location_on_grid == 0)[0]) > 0:
#             return True
#         return False
#
#     def can_piece_move(self):
#         piece_indices = self.get_piece_locations()
#         next_locations = piece_indices + self.grid.width
#         out_of_bounds = np.where(next_locations >= self.grid.width * self.grid.height)
#         if len(out_of_bounds[0]) > 0:
#             self.can_move = False
#             return False
#         piece_collision = np.where(self.grid.game_grid.flat[next_locations] == "0")
#         if len(piece_collision[0]) > 0:
#             self.can_move = False
#             return False
#         return True
#
#
# if __name__ == "__main__":
#     piece_input = input()
#     player_input = input()
#     game_grid = Grid(player_input)
#     print(game_grid.grid_to_str())
#     print()
#     piece = Piece(piece_input, game_grid)
#     game_grid.add_curr_piece(piece)
#     while player_input != "exit":
#         print(game_grid.grid_to_str(game_grid.temp_grid))
#         print()
#         player_input = input()
#         if player_input == "down":
#             piece.move_down()
#         elif player_input == "left":
#             piece.move_left()
#         elif player_input == "right":
#             piece.move_right()
#         elif player_input == "rotate":
#             piece.rotate()
#         game_grid.refresh_temp_grid()
#         piece.can_piece_move()
#
# # For this next part, reload the last instance of the board as a piece is coming down
# # then load the new location of the piece given the command
# # we need to have another array track the location of the current piece
# # maybe use pytimedinput to make this a real game?
# # Will have to restructure this tomorrow into its own classes to make it a real game
# # and easier to work with
#
# # Next time, implement borders and a floor
# # for the floor, just have a boolean switch on the piece on whether it can still move or not
# # set that to false once it hits the floor
# # then set a draw limit for whenever a location exceeds a certain value, never let the piece go past
# # the bottom
# # do rotate pushes for when a player tries to rotate once the piece is near the bottom or the sides
#
# # for move left or right, implement a check for the wall
# # for left, if a piece is already a multiple of the width, do not move left
# # for right, if a piece has a modulo of  width - 1, then cancel move right
#
# # for moving left or right, do the wall check first
# # if no wall, check the new location of all pieces (-1 or +1 for left or right)
# # check if game grid has a 0 in that location already, if so, cancel the move and continue
#
# # For moving down, as the piece gets added, it will check if the next blocks it will hit
# # is the floor or if it is a 0 on the game board. If so, piece movement will be restricted
# # and the next piece will come out
#
# # Rotations will be a bit trickier.
# # Because we know the order of how pieces rotate (always CCW), we can create a corresponding check
# # with every piece rotation. This can be incorporated into the piece_dict. This check will be responsible for
# # shifting the piece left or right after it rotates if it is up against a wall.
#
# # The bottom check should also be implemented after the rotation to see if we need to restrict piece movement.
#
# # need to implement rotation checks now. Can use the can_piece_move method within the piece.
# # only tricky rotation checks are with the line piece and L, J, S, Z, and T
# # these all have to shift in location if their rotation is within a boundary, line piece has to shift two at most
# # all other pieces only need to shift one (none have to shift up except for line piece...)
#
# # in the rotation checks for each piece. the adjustments can be stored as 1x left, 1x right, etc.
# # We can take advantage of the existing move methods without reprojecting the piece to adjust for the rotation
# # Will have to separate move_down on the left and rights and we will probably have to create a move_up
