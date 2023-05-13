# Implement the Floyd-Warshall algo
# This will find the shortest path between traversing each node, directionally
# It starts by having the known edges as the shortest paths between each node (dist[i][j] = edge[i][j])
# Then iterates through scenarios where you traverse different intermediate nodes (dist[i][k] + dist[k][j])
# and checks if that path is shorter than the current shortest path. (dist[i][j] > dist[i][k] + dist[k][j])
# If it is shorter, you record that as the new shortest distance between the two nodes.
# For every few iterations, check if the path to self (dist[i][i]) is negative. If it is, there's a negative loop
# This means that all bunnies can escape because we can increase the time indefinitely
#
# After we have all the "shortest" paths between node pairs, we need to factor in the time constraint.
# Check all permutations of bunny visits from start to finish
# Patterns to check Start -> B0 -> B1 -> ... -> Bn -> Exit
# permutation of orders, no repeats: Start -> B1 -> B0 -> ... -> Bn -> Exit
# If all bunnies do not meet the condition, decrease bunny count by one and repeat
# Get total time of each path, starting with the most bunnies
# If total time <= times_limit, return the IDs of bunnies in the path
import itertools


def find_shortest_paths(distance_matrix):  # implements Flory-Warshall algo, returns None if neg-loop
    new_distance = []
    for distances in distance_matrix:
        new_distance.append(distances[:])
    for k in range(len(new_distance)):
        for i in range(len(new_distance)):
            if new_distance[i][i] < 0:
                return None
            for j in range(len(new_distance)):
                current_distance = new_distance[i][j]
                alt_distance = new_distance[i][k] + new_distance[k][j]
                if current_distance > alt_distance:
                    new_distance[i][j] = alt_distance
    return new_distance


# Function gives paths that start with bunnies with lower number IDs
# When it is later checked for the passing condition, the function will naturally return with
# the lowest bunny IDs first (in instances where different sets of bunnies can be saved)
def create_bunny_paths(distance_matrix, num_bunnies):
    bunny_perm = itertools.permutations(range(1, len(distance_matrix) - 1), num_bunnies)
    paths = []
    for order in bunny_perm:
        new_order = [0]
        new_order.extend(order)
        new_order.append(len(distance_matrix) - 1)
        paths.append([(position, new_order[new_order.index(position) + 1]) for position in new_order[:-1]])
    return paths


def get_winning_path(distance_matrix, paths, times_limit):
    for path in paths:
        path_total_time = 0
        for start, end in path:
            path_total_time += distance_matrix[start][end]
        if path_total_time <= times_limit:
            return path
    return []


def solution(times, times_limit):
    shortest_distances = find_shortest_paths(times)
    if not shortest_distances:
        all_bunnies = []
        for i in range(0, len(times) - 2):
            all_bunnies.append(i)
        return all_bunnies  # returns all bunny IDs if there's a neg loop
    max_bunnies = len(times) - 2
    winning_path = []
    for saved_bunnies in range(max_bunnies, 0, -1):
        curr_paths = create_bunny_paths(shortest_distances, saved_bunnies)
        winning_path = get_winning_path(shortest_distances, curr_paths, times_limit)
        if winning_path:
            break
    # quick conversion of coordinates to sorted bunny IDs
    if winning_path:
        winning_set = set()
        for start, end in winning_path:
            winning_set.update({start, end})
        winning_set.remove(0)
        winning_set.remove(len(times) - 1)
        winning_list = []
        for bunny in winning_set:
            winning_list.append(bunny - 1)
        winning_list.sort()
        return winning_list
    else:
        return []



test_times = [[0, 2, 2, 2, -1],
              [9, 0, 2, 2, -1],
              [9, 3, 0, 2, -1],
              [9, 3, 2, 0, -1],
              [9, 3, 2, 2, 0]]
test_times2 = [[0, 1, 1, 1, 1],
               [1, 0, 1, 1, 1],
               [1, 1, 0, 1, 1],
               [1, 1, 1, 0, 1],
               [1, 1, 1, 1, 0]]

print(find_shortest_paths(test_times2))
print(create_bunny_paths(test_times2, len(test_times2) - 2))
print(solution(test_times2, 3))

