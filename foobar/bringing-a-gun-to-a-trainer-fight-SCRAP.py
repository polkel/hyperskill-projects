"""
Bringing a Gun to a Trainer Fight=================================

Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon
from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But
the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning
you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!
Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know
that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either
you or the bunny trainer, it will stop immediately (albeit painfully).
Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of
the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of
2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct
directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.The room
has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the
integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim].
Finally, the maximum distance that the beam can travel before becoming harmless will be given as an
integer 1 < distance <= 10000.For example, if you and the elite trainer were positioned in a room with dimensions
[3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4,
you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location):
[1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0]
is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then
the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2]
bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).

Languages=========
To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases==========
Your code should pass the following test cases.Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:Solution.solution([3,2], [1,1], [2,1], 4)Output:    7

Input:Solution.solution([300,275], [150,150], [185,100], 500)Output:    9
-- Python cases --
Input:solution.solution([300,275], [150,150], [185,100], 500)Output:    9

Input:solution.solution([3,2], [1,1], [2,1], 4)Output:    7
"""

# Thoughts:
# Use the distance formula to see if it's even possible to hit the trainer from where you are right now
# Use triangular formulas to come up with an equation?
# Find a way to create a new line from the point of reflection?
# Can also think of this in the realm of reflections (no reflection, 1 reflection, 2 reflections, 3 reflections, etc...)
# Let's lay the coordinates on top of each other

# We are going to create reflections, but in a breadth first search type of way
# Starting with the initial frame of reference, checking if the distance is fine, then reflecting the plane, N, E, S, W
# The reflection is only made if the plane reflection does not exist yet
# To identify the reflected planes, we will keep coordinates of planes. (0, 0) is the initial room, (0, 1) is N
# (0, -1) is S, (1, 0) is E, (-1, 0) is W.
# The coordinate system will be adjusted so that 0, 0 of the coordinate system is my location in plane (0, 0)
# the x and y coordinates of myself and the trainer will be stored in separate lists
# each time a new reflection is created, the distance between my (0, 0) self and the trainer reflection will be calculated
# if it's within the correct distance, checks are then made to make sure that previous reflections aren't hit
# (whether it's a reflection of me or the trainer)
# the plane is then further reflected (N, E, S, W) as long as the distance is less than the beam's effective distance
# At the end, we should have a list of all UNIQUE directions that we can hit

# Point slope form: y - y1 = m(x - x1)
# slope m = (y2 - y1) / (x2 - x1)
# line-intercept form: y = mx + b but in our case, b is always 0 since we centered ourselves on 0, 0
# distance formula is sqrt((x2 - x1)^2 + (y2 - y1)^2). In our case, x1 and y1 is always 0, 0 so..
# distance formula sqrt((x)^2 + (y)^2)
# from __future__ import division

import itertools
import math


class Plane:
    def __init__(self, plane_pos, width, height, me_pos, trainer_pos, bot_left_global=None):
        self.plane_pos = plane_pos
        self.width = width
        self.height = height
        self.me_pos = me_pos
        self.trainer_pos = trainer_pos
        if self.me_pos[0] == self.trainer_pos[0]:
            self.flip_axis()

        if bot_left_global:
            self.bot_left_global = bot_left_global
        else:
            self.bot_left_global = (-self.me_pos[0], -self.me_pos[1])

        self.me_global = (self.me_pos[0] + self.bot_left_global[0], self.me_pos[1] + self.bot_left_global[1])
        self.trainer_global = (self.trainer_pos[0] + self.bot_left_global[0], self.trainer_pos[1] + self.bot_left_global[1])

    def reflect(self, direction):
        plane_new_x = self.plane_pos[0]
        plane_new_y = self.plane_pos[1]
        me_new_x = self.me_pos[0]
        me_new_y = self.me_pos[1]
        trainer_new_x = self.trainer_pos[0]
        trainer_new_y = self.trainer_pos[1]
        bot_left_x = self.bot_left_global[0]
        bot_left_y = self.bot_left_global[1]
        if direction in "ns":
            me_new_y = self.height - me_new_y
            trainer_new_y = self.height - trainer_new_y
        else:
            me_new_x = self.width - me_new_x
            trainer_new_x = self.width - trainer_new_x

        if direction == "n":
            plane_new_y += 1
            bot_left_y += self.height
        elif direction == "s":
            plane_new_y -= 1
            bot_left_y -= self.height
        elif direction == "e":
            plane_new_x += 1
            bot_left_x += self.width
        else:
            plane_new_x -= 1
            bot_left_x -= self.width

        plane_pos = (plane_new_x, plane_new_y)
        me_pos = (me_new_x, me_new_y)
        trainer_pos = (trainer_new_x, trainer_new_y)
        bot_left_global = (bot_left_x, bot_left_y)

        return Plane(plane_pos, self.width, self.height, me_pos, trainer_pos, bot_left_global)

    def get_trainer_distance(self):
        return math.sqrt(self.trainer_global[0] ** 2 + self.trainer_global[1] ** 2)

    def get_trainer_slope(self):
        return self.trainer_global[1] / self.trainer_global[0]

    def flip_axis(self):
        width = self.height
        height = self.width
        self.width = width
        self.height = height
        self.plane_pos = self.flip_axis_coord(self.plane_pos)
        self.me_pos = self.flip_axis_coord(self.me_pos)
        self.trainer_pos = self.flip_axis_coord(self.trainer_pos)

    @staticmethod
    def flip_axis_coord(coord_tuple):
        return coord_tuple[1], coord_tuple[0]

    def get_me_global_distance(self):
        return math.sqrt((self.me_global[0]) ** 2 + (self.me_global[1]) ** 2)

    def get_trainer_global_distance(self):
        return math.sqrt((self.trainer_global[0]) ** 2 + (self.trainer_global[1]) ** 2)


def solution(dimensions, your_position, trainer_position, distance):  # convert this to just check slopes and x positive
    starting_plane = Plane((0, 0), dimensions[0], dimensions[1], tuple(your_position), tuple(trainer_position))
    all_me_pos = set()
    all_trainer_pos = set()
    all_planes = set()
    all_planes.add(starting_plane.plane_pos)
    current_planes = [starting_plane]
    count = 0
    while current_planes:
        print(count)
        new_planes = []
        for plane in current_planes:
            if plane.get_trainer_distance() > distance:
                continue
            if plane.me_global != (0, 0):
                all_me_pos.add(plane.me_global)
            self_collision = False
            slope = plane.get_trainer_slope()  # We need to handle infinite slope! Let's handle it from a class level
            trainer_y = plane.trainer_global[1]
            trainer_x = plane.trainer_global[0]
            for x, y in all_me_pos.union(all_trainer_pos):
                if y == slope * x and y * trainer_y >= 0 and x * trainer_x >= 0:  # last two conditions check directionality
                    self_collision = True
                    break
            if not self_collision:
                all_trainer_pos.add(plane.trainer_global)
            for direction in "nesw":
                new_plane = plane.reflect(direction)
                if new_plane.plane_pos not in all_planes:
                    all_planes.add(new_plane.plane_pos)
                    new_planes.append(new_plane)
        current_planes = new_planes
        count += 1
    return len(all_trainer_pos)


# print(solution([3, 3], [1, 1], [1, 2], 20))


# def test():
#     assert solution([3, 2], [1, 1], [2, 1], 4) == 7
#     assert solution([2, 5], [1, 2], [1, 4], 11) == 27
#     assert solution([23, 10], [6, 4], [3, 2], 23) == 8
#     assert solution([1250, 1250], [1000, 1000], [500, 400], 10000) == 196
#     assert solution([10, 10], [4, 4], [3, 3], 5000) == 739323
#     assert solution([3, 2], [1, 1], [2, 1], 7) == 19
#     assert solution([2, 3], [1, 1], [1, 2], 4) == 7
#     assert solution([3, 4], [1, 2], [2, 1], 7) == 10
#     assert solution([4, 4], [2, 2], [3, 1], 6) == 7
#     assert solution([300, 275], [150, 150], [180, 100], 500) == 9
#     assert solution([3, 4], [1, 1], [2, 2], 500) == 54243




# to generate all trainer positions
def solution2(dimensions, your_position, trainer_position, distance):
    width = dimensions[0]
    height = dimensions[1]
    me_x = your_position[0]
    me_y = your_position[1]
    me_pairs = get_all_coords(dimensions, your_position, distance, your_position)
    trainer_pairs = get_all_coords(dimensions, trainer_position, distance, your_position)
    print(len(trainer_pairs))
    print(len(me_pairs))
    count = 0
    vetted_pairs = set()
    for dist, ang in trainer_pairs:
        my_filter = filter(lambda pair: pair[0] < dist and pair[1] == ang, me_pairs)
        print(count)
        collision = False
        for item in my_filter:
            collision = True
            break
        # for dist_2, ang_2 in me_pairs.union(vetted_pairs):
        #     if ang == ang_2 and dist_2 < dist:
        #         collision = True
        #         break
        if not collision:
            vetted_pairs.add((dist, ang))
        count += 1
    print(len(vetted_pairs))


def get_all_coords(dimensions, position, distance, compare):  # returns all reflection coordinates within distance
    width = dimensions[0]
    height = dimensions[1]
    x = position[0]
    y = position[1]
    dist_x = compare[0]
    dist_y = compare[1]
    pos_x_limit = dist_x + distance + 1
    neg_x_limit = dist_x - distance - 1
    pos_y_limit = dist_y + distance + 1
    neg_y_limit = dist_y - distance - 1
    x_pos_1 = range(x, pos_x_limit, width * 2)
    x_pos_2 = range(2 * width - x, pos_x_limit, width * 2)  # these are the reflection x coords
    x_neg_1 = range(-x, neg_x_limit, width * -2)
    x_neg_2 = range(-2 * width + x, neg_x_limit, width * -2)
    y_pos_1 = range(y, pos_y_limit, height * 2)
    y_pos_2 = range(2 * height - y, pos_y_limit, height * 2)
    y_neg_1 = range(-y, neg_y_limit, height * -2)
    y_neg_2 = range(-2 * height + y, neg_y_limit, height * -2)
    all_x = itertools.chain(x_neg_2, x_neg_1, x_pos_1, x_pos_2)
    all_y = itertools.chain(y_neg_2, y_neg_1, y_pos_1, y_pos_2)
    all_pairs = itertools.product(all_x, all_y)
    all_pairs = map(lambda pair: (pair[0] - dist_x, pair[1] - dist_y), all_pairs)
    all_pairs = list(all_pairs)
    all_pairs.sort(key=lambda pair: math.sqrt(pair[0] ** 2 + pair[1] ** 2))
    final_dists = []
    final_angles = []
    for i, j in all_pairs:
        angle = math.atan2(j, i)
        if i == 0 and j == 0 or math.atan2(j, i) in final_angles:
            continue
        final_angles.append(angle)
        final_dists.append(math.sqrt(i ** 2 + j ** 2))
    return set(zip(final_dists, final_angles))
    all_pairs = filter(lambda coord: math.sqrt((coord[0]) ** 2 + (coord[1]) ** 2) <= distance, all_pairs)
    all_dist_angles = map(convert_to_angle_distance,
                          all_pairs)
    all_coords = set(all_dist_angles)
    # all_coords = list(all_coords)
    # all_coords.sort(key=lambda coord: math.sqrt((coord[0] - dist_x) ** 2 + (coord[1] - dist_y) ** 2))
    return all_coords


def convert_to_angle_distance(coord):
    return math.sqrt(coord[0] ** 2 + coord[1] ** 2), math.atan2(coord[1], coord[0])


def solution3(dimensions, your_position, trainer_position, distance):  # convert this to just check slopes and x positive
    starting_plane = Plane((0, 0), dimensions[0], dimensions[1], tuple(your_position), tuple(trainer_position))
    all_me_pos = set()
    all_trainer_pos = set()
    all_planes = set()
    all_planes.add(starting_plane.plane_pos)
    current_planes = [starting_plane]
    count = 0
    while current_planes:
        print(count)
        new_planes = []
        for plane in current_planes:
            if plane.get_trainer_distance() > distance:
                continue
            if plane.me_global != (0, 0) and plane.me_global[
                0] != 0 and plane.get_me_global_distance() < plane.get_trainer_global_distance():
                is_x_pos = bool(plane.me_global[0] > 0)
                all_me_pos.add((plane.me_global[1] / plane.me_global[0], is_x_pos))
            slope = plane.get_trainer_slope()  # We need to handle infinite slope! Let's handle it from a class level
            trainer_x = plane.trainer_global[0]
            is_x_trainer_pos = bool(trainer_x > 0)
            trainer_pos = (slope, is_x_trainer_pos)
            if trainer_pos not in all_me_pos.union(all_trainer_pos):
                all_trainer_pos.add(trainer_pos)
            directions = []
            plane_x = plane.plane_pos[0]
            plane_y = plane.plane_pos[1]
            if (plane_x, plane_y + 1) not in all_planes:
                directions.append("n")
                all_planes.add((plane_x, plane_y + 1))
            if (plane_x, plane_y - 1) not in all_planes:
                directions.append("s")
                all_planes.add((plane_x, plane_y - 1))
            if (plane_x + 1, plane_y) not in all_planes:
                directions.append("e")
                all_planes.add((plane_x + 1, plane_y))
            if (plane_x - 1, plane_y) not in all_planes:
                directions.append("w")
                all_planes.add((plane_x - 1, plane_y))
            for direction in directions:
                new_plane = plane.reflect(direction)
                new_planes.append(new_plane)
            if plane.me_global != (0, 0) and plane.me_global[
                0] != 0 and plane.get_me_global_distance() > plane.get_trainer_global_distance():
                is_x_pos = bool(plane.me_global[0] > 0)
                all_me_pos.add((plane.me_global[1] / plane.me_global[0], is_x_pos))
        count += 1
        print(len(new_planes))
        current_planes = new_planes
    return len(all_trainer_pos)


# Starting from top right, ccw, q1 - q4. Planes landing in cardinal directions are not part of a quadrant
# Find iterations in cardinal directions first, then q1, q2, q3, q4
# If in a cardinal direction the coordinate is the same, it's only 1 iteration, otherwise all iterations
# For quadrants, we will have to do it iteratively
# Store all angles in a set?
def new_solution(coordinates, old_my_place, old_trainer_place, distance):

    width = coordinates[0]
    height = coordinates[1]
    trainer_place = [old_trainer_place[0] - old_my_place[0], old_trainer_place[1] - old_my_place[1]]
    count = 1
    my_slope = set()
    if 0 not in trainer_place:
        my_slope.add(float(trainer_place[1]) / trainer_place[0])

    n_slopes, n_count = find_cardinal_slope_count(trainer_place, height, distance)
    e_slopes, e_count = find_cardinal_slope_count(trainer_place, width, distance, east=True)
    count += n_count * 2 + e_count * 2  # origin plane and cardinal reflections accounted for



    print(count, my_slope, n_slopes, e_slopes)


def find_cardinal_slope_count(trainer_coord, dimension, distance, east=False):  # return slopes and added counts
    count = 0
    slopes = set()

    if east:
        active_dir = trainer_coord[0]
        passive_dir = trainer_coord[1]
    else:
        active_dir = trainer_coord[1]
        passive_dir = trainer_coord[0]

    if passive_dir != 0:
        limit = math.sqrt(distance ** 2 - passive_dir ** 2)
        limit = math.ceil(limit)
        set_1 = range(dimension * 2 - active_dir, limit, dimension * 2)
        set_2 = range(active_dir + 2 * dimension, limit, dimension * 2)
        count = len(set_1) + len(set_2)
        slopes = set()
        chain = itertools.chain(set_1, set_2)
        passive_coord = float(passive_dir)
        for num in chain:
            if east:
                slopes.add(passive_coord / num)
            else:
                slopes.add(num / passive_coord)

    return slopes, count


def find_distance(coord):
    return math.sqrt(coord[0] ** 2 + coord[1] ** 2)


def new_new_solution(dimension, mine, yours, distance):
    # same approach get cardinal directions first, no transformations
    initial_distance = math.sqrt((yours[0] - mine[0]) ** 2 + (yours[1] - mine[1]) ** 2)
    if distance < initial_distance:
        return 0
    me_pos_x, me_neg_x, me_pos_y, me_neg_y = get_limits(dimension, mine, distance, mine)
    you_pos_x, you_neg_x, you_pos_y, you_neg_y = get_limits(dimension, yours, distance, mine)
    print(len(you_pos_x), len(you_neg_x), len(you_pos_y), len(you_neg_y))
    print(you_pos_x[-3:], you_neg_x[-3:], you_pos_y[-3:], you_neg_y[-3:])
    print(len(me_pos_x), len(me_neg_x), len(me_pos_y), len(me_neg_y))

    # count self
    count = 1
    my_direction = set()
    if mine[0] != yours[0] and mine[1] != yours[1]:
        my_direction.add(calc_direction(mine, yours))

    # check north-south first
    n_directions = set()
    s_directions = set()
    if mine[0] != yours[0]:
        for y in you_pos_y[1:]:
            n_directions.add(calc_direction(mine, [yours[0], y]))
        count += len(n_directions)
        for y in you_neg_y:
            s_directions.add(calc_direction(mine, [yours[0], y]))
        count += len(s_directions)

    # check east-west
    e_directions = set()
    w_directions = set()
    if mine[1] != yours[1]:
        for x in you_pos_x[1:]:
            e_directions.add(calc_direction(mine, [x, yours[1]]))
        count += len(e_directions)
        for x in you_neg_x:
            w_directions.add(calc_direction(mine, [x, yours[1]]))
        count += len(w_directions)

    # do q1
    ah_fuck = 0
    starting_planes = set()
    all_planes = set()
    if 1 < len(you_pos_x) and 1 < len(you_pos_y):
        starting_planes.add((1, 1))
    directions_to_check = my_direction.union(n_directions).union(e_directions)
    while starting_planes:
        new_planes = set()
        for plane in starting_planes:
            plane_x = plane[0]
            plane_y = plane[1]
            me_coord = [me_pos_x[plane_x], me_pos_y[plane_y]]
            you_coord = [you_pos_x[plane_x], you_pos_y[plane_y]]
            curr_plane = Plane2(plane, me_coord, you_coord, mine)
            if curr_plane.get_distance() <= distance:
                if plane_x + 1 < len(you_pos_x):
                    new_planes.add((plane_x + 1, plane_y))
                if plane_y + 1 < len(you_pos_y):
                    new_planes.add((plane_x, plane_y + 1))
                if curr_plane.get_you_direction() not in directions_to_check:
                    count += 1
                    if curr_plane.get_you_direction() == curr_plane.get_me_direction():
                        print("AHHH FUCK")
                        print(f"Me distance: {curr_plane.get_me_distance()}, You distance: {curr_plane.get_distance()}")
                        if curr_plane.get_me_distance() < curr_plane.get_distance():
                            count -= 1
                            ah_fuck += 1
            directions_to_check.add(curr_plane.get_you_direction())
            directions_to_check.add(curr_plane.get_me_direction())
        all_planes.update(starting_planes)
        starting_planes = new_planes

    # do q2
    starting_planes = set()
    all_planes = set()
    if 0 < len(you_neg_x) and 1 < len(you_pos_y):
        starting_planes.add((0, 1))
    directions_to_check = my_direction.union(n_directions).union(w_directions)
    while starting_planes:
        new_planes = set()
        for plane in starting_planes:
            plane_x = plane[0]
            plane_y = plane[1]
            me_coord = [me_neg_x[plane_x], me_pos_y[plane_y]]
            you_coord = [you_neg_x[plane_x], you_pos_y[plane_y]]
            curr_plane = Plane2(plane, me_coord, you_coord, mine)
            if curr_plane.get_distance() <= distance:
                if plane_x + 1 < len(you_neg_x):
                    new_planes.add((plane_x + 1, plane_y))
                if plane_y + 1 < len(you_pos_y):
                    new_planes.add((plane_x, plane_y + 1))
                if curr_plane.get_you_direction() not in directions_to_check:
                    count += 1
                    if curr_plane.get_you_direction() == curr_plane.get_me_direction():
                        print("AHHH FUCK")
                        print(f"Me distance: {curr_plane.get_me_distance()}, You distance: {curr_plane.get_distance()}")
                        if curr_plane.get_me_distance() < curr_plane.get_distance():
                            count -= 1
                            ah_fuck += 1
            directions_to_check.add(curr_plane.get_you_direction())
            directions_to_check.add(curr_plane.get_me_direction())
        all_planes.update(starting_planes)
        starting_planes = new_planes

    # do q3
    starting_planes = set()
    all_planes = set()
    if 0 < len(you_neg_x) and 0 < len(you_neg_y):
        starting_planes.add((0, 0))
    directions_to_check = my_direction.union(s_directions).union(w_directions)
    while starting_planes:
        new_planes = set()
        for plane in starting_planes:
            plane_x = plane[0]
            plane_y = plane[1]
            me_coord = [me_neg_x[plane_x], me_neg_y[plane_y]]
            you_coord = [you_neg_x[plane_x], you_neg_y[plane_y]]
            curr_plane = Plane2(plane, me_coord, you_coord, mine)
            if curr_plane.get_distance() <= distance:
                if curr_plane.you_coord == [-352, -350]:
                    print("WE HIT")
                if plane_x + 1 < len(you_neg_x):
                    new_planes.add((plane_x + 1, plane_y))
                if plane_y + 1 < len(you_neg_y):
                    new_planes.add((plane_x, plane_y + 1))
                if curr_plane.get_you_direction() not in directions_to_check:
                    count += 1
                    if curr_plane.get_you_direction() == curr_plane.get_me_direction():
                        print("AHHH FUCK")
                        print(f"Me distance: {curr_plane.get_me_distance()}, You distance: {curr_plane.get_distance()}")
                        if curr_plane.get_me_distance() < curr_plane.get_distance():
                            count -= 1
                            ah_fuck += 1
            directions_to_check.add(curr_plane.get_you_direction())
            directions_to_check.add(curr_plane.get_me_direction())
        all_planes.update(starting_planes)
        starting_planes = new_planes

    # do q4
    if -352 in you_neg_x and -350 in you_neg_y:
        print("its a hit")

    starting_planes = set()
    all_planes = set()
    if 1 < len(you_pos_x) and 0 < len(you_neg_y):
        starting_planes.add((1, 0))
    directions_to_check = my_direction.union(s_directions).union(e_directions)
    while starting_planes:
        new_planes = set()
        for plane in starting_planes:
            plane_x = plane[0]
            plane_y = plane[1]
            me_coord = [me_pos_x[plane_x], me_neg_y[plane_y]]
            you_coord = [you_pos_x[plane_x], you_neg_y[plane_y]]
            curr_plane = Plane2(plane, me_coord, you_coord, mine)
            if curr_plane.get_distance() <= distance:
                if plane_x + 1 < len(you_pos_x):
                    new_planes.add((plane_x + 1, plane_y))
                if plane_y + 1 < len(you_neg_y):
                    new_planes.add((plane_x, plane_y + 1))
                if curr_plane.get_you_direction() not in directions_to_check:
                    count += 1
                    if curr_plane.get_you_direction() == curr_plane.get_me_direction():
                        print("AHHH FUCK")
                        print(f"Me distance: {curr_plane.get_me_distance()}, You distance: {curr_plane.get_distance()}")
                        if curr_plane.get_me_distance() < curr_plane.get_distance():
                            count -= 1
                            ah_fuck += 1
            directions_to_check.add(curr_plane.get_you_direction())
            directions_to_check.add(curr_plane.get_me_direction())
        all_planes.update(starting_planes)
        starting_planes = new_planes
    return count


def calc_direction(origin, dest):
    return math.atan2(dest[1] - origin[1], dest[0] - origin[0])


def get_limits(dimension, coord, distance, comparison):
    w = dimension[0]
    h = dimension[1]
    y_pos_limit = math.floor(math.sqrt(distance ** 2 - (coord[0] - comparison[0]) ** 2) + comparison[1] + 1)
    y_pos_limit = int(y_pos_limit)
    x_pos_limit = math.floor(1 + comparison[0] + math.sqrt(distance ** 2 - (coord[1] - comparison[1]) ** 2))
    x_pos_limit = int(x_pos_limit)
    y_neg_limit = math.ceil(comparison[1] - math.sqrt(distance ** 2 - (coord[0] - comparison[0]) ** 2) - 1)
    y_neg_limit = int(y_neg_limit)
    x_neg_limit = math.ceil(comparison[0] - math.sqrt(distance ** 2 - (coord[1] - comparison[1]) ** 2) - 1)
    x_neg_limit = int(x_neg_limit)
    y_pos_1 = range(coord[1], y_pos_limit, int(h * 2))
    y_pos_2 = range(h * 2 - coord[1], y_pos_limit, int(h * 2))
    x_pos_1 = range(coord[0], x_pos_limit, int(w * 2))
    x_pos_2 = range(w * 2 - coord[0], x_pos_limit, int(w * 2))
    y_pos_chain = itertools.chain(y_pos_1, y_pos_2)
    y_pos_list = list(y_pos_chain)
    y_pos_list.sort()
    x_pos_chain = itertools.chain(x_pos_1, x_pos_2)
    x_pos_list = list(x_pos_chain)
    x_pos_list.sort()

    y_neg_1 = range(-coord[1], y_neg_limit, int(h * -2))
    y_neg_2 = range(h * -2 + coord[1], y_neg_limit, int(h * -2))
    x_neg_1 = range(-coord[0], x_neg_limit, int(w * -2))
    x_neg_2 = range(w * -2 + coord[0], x_neg_limit, int(w * -2))
    y_neg_chain = itertools.chain(y_neg_1, y_neg_2)
    y_neg_list = list(y_neg_chain)
    y_neg_list.sort(reverse=True)
    x_neg_chain = itertools.chain(x_neg_1, x_neg_2)
    x_neg_list = list(x_neg_chain)
    x_neg_list.sort(reverse=True)

    return x_pos_list, x_neg_list, y_pos_list, y_neg_list


class Plane2:
    def __init__(self, plane_pos, me_coord, you_coord, origin):
        self.plane_pos = plane_pos
        self.me_coord = me_coord
        self.you_coord = you_coord
        self.origin = origin

    def get_distance(self):
        return math.sqrt((self.you_coord[0] - self.origin[0]) ** 2 + (self.you_coord[1] - self.origin[1]) ** 2)

    def get_you_direction(self):
        return calc_direction(self.origin, self.you_coord)

    def get_me_direction(self):
        return calc_direction(self.origin, self.me_coord)

    def get_me_distance(self):
        return math.sqrt((self.me_coord[0] - self.origin[0]) ** 2 + (self.me_coord[1] - self.origin[1]) ** 2)


def my_last_attempt(dimension, me, you, distance):
    # first we get all the x and y's at the absolute limit for both me and you
    me_points = generate_points(dimension, me, me, distance, "me")
    you_points = generate_points(dimension, you, me, distance, "you")
    all_points = me_points + you_points
    all_points.sort(key=lambda item: get_distance(me, item[0]))
    count = 0
    directions = set()
    for point, tag in all_points:
        if get_distance(me, point) > distance:
            break
        curr_direction = get_direction(me, point)
        if curr_direction in directions:
            continue
        else:
            directions.add(curr_direction)
            if tag == "you":
                count += 1

    print(count)
    return count


def generate_points(dimension, entity, comparison, distance, tag):
    w = dimension[0]
    h = dimension[1]
    comp_x = comparison[0]
    comp_y = comparison[1]
    entity_x = entity[0]
    entity_y = entity[1]
    x_limit_pos = comp_x + distance + 1
    x_limit_neg = comp_x - distance - 1
    y_limit_pos = comp_y + distance + 1
    y_limit_neg = comp_y - distance - 1

    x_pos_1 = range(entity_x, x_limit_pos, w * 2)
    x_pos_2 = range(w * 2 - entity_x, x_limit_pos, w * 2)
    x_neg_1 = range(-entity_x, x_limit_neg, w * -2)
    x_neg_2 = range(w * -2 + entity_x, x_limit_neg, w * -2)
    all_x = itertools.chain(x_pos_1, x_pos_2, x_neg_1, x_neg_2)

    y_pos_1 = range(entity_y, y_limit_pos, h * 2)
    y_pos_2 = range(h * 2 - entity_y, y_limit_pos, h * 2)
    y_neg_1 = range(-entity_y, y_limit_neg, h * -2)
    y_neg_2 = range(h * -2 + entity_y, y_limit_neg, h * -2)
    all_y = itertools.chain(y_pos_1, y_pos_2, y_neg_1, y_neg_2)
    all_y = set(all_y)

    all_points = list()

    for x in all_x:
        for y in all_y:
            if x == comp_x and y == comp_y:
                continue
            all_points.append(((x, y), tag))

    return all_points


def get_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


def get_direction(origin, comparison):
    return math.atan2(comparison[1] - origin[1], comparison[0] - origin[0])


my_last_attempt([3, 2], [1, 1], [2, 1], 4)
my_last_attempt([2, 5], [1, 2], [1, 4], 11)
my_last_attempt([23, 10], [6, 4], [3, 2], 23)
my_last_attempt([1250, 1250], [1000, 1000], [500, 400], 10000)
my_last_attempt([10, 10], [4, 4], [3, 3], 5000)
my_last_attempt([3, 2], [1, 1], [2, 1], 7)
my_last_attempt([2, 3], [1, 1], [1, 2], 4)
my_last_attempt([3, 4], [1, 2], [2, 1], 7)
my_last_attempt([4, 4], [2, 2], [3, 1], 6)
my_last_attempt([300, 275], [150, 150], [180, 100], 500)
my_last_attempt([3, 4], [1, 1], [2, 2], 500)


# def test():
#     assert solution([3, 2], [1, 1], [2, 1], 4) == 7
#     assert solution([2, 5], [1, 2], [1, 4], 11) == 27
#     assert solution([23, 10], [6, 4], [3, 2], 23) == 8
#     assert solution([1250, 1250], [1000, 1000], [500, 400], 10000) == 196
#     assert solution([10, 10], [4, 4], [3, 3], 5000) == 739323
#     assert solution([3, 2], [1, 1], [2, 1], 7) == 19
#     assert solution([2, 3], [1, 1], [1, 2], 4) == 7
#     assert solution([3, 4], [1, 2], [2, 1], 7) == 10
#     assert solution([4, 4], [2, 2], [3, 1], 6) == 7
#     assert solution([300, 275], [150, 150], [180, 100], 500) == 9
#     assert solution([3, 4], [1, 1], [2, 2], 500) == 54243


"""
OLD
from __future__ import division
import math


class Plane:
    def __init__(self, plane_pos, width, height, me_pos, trainer_pos, bot_left_global=None):
        self.plane_pos = plane_pos
        self.width = width
        self.height = height
        self.me_pos = me_pos
        self.trainer_pos = trainer_pos
        if self.me_pos[0] == self.trainer_pos[0]:  # this makes the trajectory horizontal, if slope is infinite
            self.flip_axis()

        if bot_left_global:
            self.bot_left_global = bot_left_global
        else:
            self.bot_left_global = (-self.me_pos[0], -self.me_pos[1])

        self.me_global = (self.me_pos[0] + self.bot_left_global[0], self.me_pos[1] + self.bot_left_global[1])
        self.trainer_global = (self.trainer_pos[0] + self.bot_left_global[0], self.trainer_pos[1] + self.bot_left_global[1])

    def reflect(self, direction):
        plane_new_x = self.plane_pos[0]
        plane_new_y = self.plane_pos[1]
        me_new_x = self.me_pos[0]
        me_new_y = self.me_pos[1]
        trainer_new_x = self.trainer_pos[0]
        trainer_new_y = self.trainer_pos[1]
        bot_left_x = self.bot_left_global[0]
        bot_left_y = self.bot_left_global[1]
        if direction in "ns":
            me_new_y = self.height - me_new_y
            trainer_new_y = self.height - trainer_new_y
        else:
            me_new_x = self.width - me_new_x
            trainer_new_x = self.width - trainer_new_x

        if direction == "n":
            plane_new_y += 1
            bot_left_y += self.height
        elif direction == "s":
            plane_new_y -= 1
            bot_left_y -= self.height
        elif direction == "e":
            plane_new_x += 1
            bot_left_x += self.width
        else:
            plane_new_x -= 1
            bot_left_x -= self.width

        plane_pos = (plane_new_x, plane_new_y)
        me_pos = (me_new_x, me_new_y)
        trainer_pos = (trainer_new_x, trainer_new_y)
        bot_left_global = (bot_left_x, bot_left_y)

        return Plane(plane_pos, self.width, self.height, me_pos, trainer_pos, bot_left_global)

    def get_trainer_distance(self):
        return math.sqrt(self.trainer_global[0] ** 2 + self.trainer_global[1] ** 2)

    def get_trainer_slope(self):
        return float(self.trainer_global[1]) / self.trainer_global[0]

    def flip_axis(self):
        width = self.height
        height = self.width
        self.width = width
        self.height = height
        self.plane_pos = self.flip_axis_coord(self.plane_pos)
        self.me_pos = self.flip_axis_coord(self.me_pos)
        self.trainer_pos = self.flip_axis_coord(self.trainer_pos)

    @staticmethod
    def flip_axis_coord(coord_tuple):
        return coord_tuple[1], coord_tuple[0]
        
    def get_me_global_distance(self):
        return math.sqrt((self.me_global[0]) ** 2 + (self.me_global[1]) ** 2)
        
    def get_trainer_global_distance(self):
        return math.sqrt((self.trainer_global[0]) ** 2 + (self.trainer_global[1]) ** 2)


def solution(dimensions, your_position, trainer_position, distance):
    starting_plane = Plane((0, 0), dimensions[0], dimensions[1], tuple(your_position), tuple(trainer_position))
    all_me_pos = set()
    all_trainer_pos = set()
    all_planes = set()
    all_planes.add(starting_plane.plane_pos)
    current_planes = [starting_plane]
    while current_planes:
        new_planes = []
        for plane in current_planes:
            if plane.get_trainer_distance() > distance:
                continue
            if plane.me_global != (0, 0) and plane.me_global[0] != 0 and plane.get_me_global_distance() < plane.get_trainer_global_distance():
                is_x_pos = bool(plane.me_global[0] > 0)
                all_me_pos.add((float(plane.me_global[1]) / plane.me_global[0], is_x_pos))
            slope = plane.get_trainer_slope()  # We need to handle infinite slope! Let's handle it from a class level
            trainer_x = plane.trainer_global[0]
            is_x_trainer_pos = bool(trainer_x > 0)
            trainer_pos = (slope, is_x_trainer_pos)
            if trainer_pos not in all_me_pos.union(all_trainer_pos):
                all_trainer_pos.add(trainer_pos)
            directions = []
            plane_x = plane.plane_pos[0]
            plane_y = plane.plane_pos[1]
            if (plane_x, plane_y + 1) not in all_planes:
                directions.append("n")
                all_planes.add((plane_x, plane_y + 1))
            if (plane_x, plane_y - 1) not in all_planes:
                directions.append("s")
                all_planes.add((plane_x, plane_y - 1))
            if (plane_x + 1, plane_y) not in all_planes:
                directions.append("e")
                all_planes.add((plane_x + 1, plane_y))
            if (plane_x - 1, plane_y) not in all_planes:
                directions.append("w")
                all_planes.add((plane_x - 1, plane_y))
            for direction in directions:
                new_plane = plane.reflect(direction)
                new_planes.append(new_plane)
            if plane.me_global != (0, 0) and plane.me_global[0] != 0 and plane.get_me_global_distance() > plane.get_trainer_global_distance():
                is_x_pos = bool(plane.me_global[0] > 0)
                all_me_pos.add((float(plane.me_global[1]) / plane.me_global[0], is_x_pos))
        current_planes = new_planes
    return len(all_trainer_pos)

"""