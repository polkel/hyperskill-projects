"""

Prepare the Bunnies' Escape===========================

You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander Lambda's bunny workers, but once they're free of the work duties the bunnies are going to need to escape Lambda's space station via the escape pods as quickly as possible. Unfortunately, the halls of the space station are a maze of corridors and dead ends that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling project that will give you the opportunity to make things a little easier for the bunnies. Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions. You have maps of parts of the space station, each starting at a work area exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1). Write a function solution(map) that generates the length of the shortest path from the station door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.

Languages=========
To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases==========
Your code should pass the following test cases.Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:solution.solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])Output:    11

Input:solution.solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])Output:    7
-- Java cases --
Input:Solution.solution({{0, 1, 1, 0}, {0, 0, 0, 1}, {1, 1, 0, 0}, {1, 1, 1, 0}})Output:    7

Input:Solution.solution({{0, 0, 0, 0, 0, 0}, {1, 1, 1, 1, 1, 0}, {0, 0, 0, 0, 0, 0}, {0, 1, 1, 1, 1, 1}, {0, 1, 1, 1, 1, 1}, {0, 0, 0, 0, 0, 0}})Output:    11

"""


# Maze solving algorithm:
# 1. Set starting node (0, 0) as current node, initialize count at 0
# 2. From current node(s), find all eligible neighbors to traverse (N, E, S, W)
# eligibility: coordinate is not a wall/boundary and is not in the visited set
# 3. Put current node(s) in the visited set, increment count by 1
# 4. Set new eligible neighbors as current node(s)
# 5. Repeat steps 2-4 until the ending coordinate (w - 1, h - 1) is in neighbors
# 6. Return count + 1

# Optimal walls to remove
# Find all walls that have at least 2 adjacent "0" values. If only 1, there's no point in removing it


class Maze:
    def __init__(self, maze):
        self.maze = maze
        self.width = len(maze)
        self.height = len(maze[0])
        self.walls_to_remove = self.find_walls_to_remove()
        self.visited = set()

    def look(self, direction, x, y):  # 0 for path, 1 for wall, -1 for boundary
        check_x = x
        check_y = y

        if direction == "n":
            check_y -= 1
            condition = check_y >= 0
        elif direction == "s":
            check_y += 1
            condition = check_y < self.height
        elif direction == "w":
            check_x -= 1
            condition = check_x >= 0
        else:
            check_x += 1
            condition = check_x < self.width

        if condition:
            return self.maze[check_x][check_y]
        else:
            return -1

    def find_walls_to_remove(self):
        walls_to_remove = []
        for i in range(0, self.width):
            for j in range(0, self.height):
                if self.maze[i][j] == 1:
                    wall_sum = abs(self.look("n", i, j))
                    wall_sum += abs(self.look("e", i, j))
                    wall_sum += abs(self.look("s", i, j))
                    wall_sum += abs(self.look("w", i, j))
                    if wall_sum < 3:
                        walls_to_remove.append((i, j))
        return walls_to_remove

    def copy_maze(self):
        maze_copy = []
        for column in self.maze:
            maze_copy.append(column[:])
        return maze_copy

    def find_eligible_neighbors(self, coordinate_tuple):
        neighbors = set()
        x, y = coordinate_tuple
        north = (x, y -1)
        east = (x + 1, y)
        south = (x, y + 1)
        west = (x - 1, y)
        if not self.look("n", x, y) and north not in self.visited:
            neighbors.add(north)
        if not self.look("e", x, y) and east not in self.visited:
            neighbors.add(east)
        if not self.look("s", x, y) and south not in self.visited:
            neighbors.add(south)
        if not self.look("w", x, y) and west not in self.visited:
            neighbors.add(west)
        return neighbors

    def find_shortest_path(self):
        neighbors = set()
        neighbors.add((0, 0))
        count = 0
        while (self.width - 1, self.height - 1) not in neighbors:
            new_neighbors = set()
            for coordinate in neighbors:
                new_neighbors.update(self.find_eligible_neighbors(coordinate))
            count += 1
            self.visited.update(neighbors)
            if not new_neighbors:
                return None
            neighbors = new_neighbors
        return count + 1


def solution(maze):
    my_maze = Maze(maze)
    curr_min = my_maze.find_shortest_path()
    for x, y in my_maze.walls_to_remove:
        wall_removed = my_maze.copy_maze()
        wall_removed[x][y] = 0
        new_maze = Maze(wall_removed)
        temp_min = new_maze.find_shortest_path()
        if curr_min and temp_min:
            if temp_min < curr_min:
                curr_min = temp_min
        elif not curr_min and temp_min:
            curr_min = temp_min
    return curr_min


test_maze = [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]

print(solution(test_maze))
