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


import itertools
import math


def solution(dimension, me, you, distance):
    # Get all points within the absolute limit for both me and you
    me_points = generate_points(dimension, me, me, distance, "me")
    you_points = generate_points(dimension, you, me, distance, "you")
    # Combine all possible reflections and sort by distance from self
    all_points = me_points + you_points
    all_points.sort(key=lambda item: get_distance(me, item[0]))
    count = 0
    directions = set()  # Directions set will be used to check for redundancy
    for point, tag in all_points:
        if get_distance(me, point) > distance:
            break  # Stop checking once points are beyond laser distance
        curr_direction = get_direction(me, point)
        if curr_direction in directions:
            continue  # If we have already hit something in this direction, skip this iteration
        else:
            directions.add(curr_direction)
            if tag == "you":
                count += 1  # Only add trainer hits to the count

    return count


def generate_points(dimension, entity, comparison, distance, tag):
    # This generates all possible reflection points within a distance from 'comparison'
    # 'tag' is used to identify self or trainer
    w = dimension[0]
    h = dimension[1]
    comp_x = comparison[0]
    comp_y = comparison[1]
    entity_x = entity[0]
    entity_y = entity[1]
    # Any x or y points beyond limits below will exceed laser distance
    x_limit_pos = comp_x + distance + 1
    x_limit_neg = comp_x - distance - 1
    y_limit_pos = comp_y + distance + 1
    y_limit_neg = comp_y - distance - 1

    # In reflections, room-relative x and y are the same every 2 reflections in any cardinal direction
    # Find all possible x and y values through incrementing 2 * width or 2 * height
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
            if x == comp_x and y == comp_y:  # Excludes comparison point in the list
                continue
            all_points.append(((x, y), tag))

    return all_points


def get_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


def get_direction(origin, comparison):
    return math.atan2(comparison[1] - origin[1], comparison[0] - origin[0])
