import sys
from utils import *
from priority_queue import PriorityQueue


def is_valid_move(graph, bounded_row, bounded_col):
    row, col = bounded_row + 1, bounded_col + 1
    for (r, c) in [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                   (row, col - 1), (row, col), (row, col + 1),
                   (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]:
        if 0 <= r <= 19 and 0 <= c <= 14 and graph[r][c] == 1:
            return False

    return True


def turning_cost(before_point, current_point, next_point):
    if before_point is None:
        return 1
    else:
        if (before_point[0] == current_point[0] == next_point[0] or
                before_point[1] == current_point[1] == next_point[1]):
            return 1
        else:
            return 3


def find_fastest_path(graph, start_point=(1, 1), goal_point=(18, 13), before_start_point=None):
    bounded_start_point = (start_point[0] - 1, start_point[1] - 1)
    bounded_goal_point = (goal_point[0] - 1, goal_point[1] - 1)
    if before_start_point is None:
        bounded_before_start_point = bounded_start_point
    else:
        bounded_before_start_point = (before_start_point[0] - 1, before_start_point[1] - 1)

    results = []
    bounded_graph = [graph[i][1:14] for i in range(1, 19)]

    discovers = [[0 for i in range(13)] for j in range(18)]
    distances_from_start = [[sys.maxsize for i in range(13)] for j in range(18)]
    distances_to_goal = [[0 for i in range(13)] for j in range(18)]
    cost = [[0 for i in range(13)] for j in range(18)]
    before = [[None for i in range(13)] for j in range(18)]
    q = PriorityQueue()

    distances_from_start[bounded_start_point[0]][bounded_start_point[1]] = 0
    before[bounded_start_point[0]][bounded_start_point[1]] = bounded_before_start_point
    for row in range(len(bounded_graph)):
        for col in range(len(bounded_graph[row])):
            distances_to_goal[row][col] = abs(row - bounded_goal_point[0]) + abs(col - bounded_goal_point[1])
            cost[row][col] = distances_from_start[row][col] + distances_to_goal[row][col]
            q[(row, col)] = cost[row][col]

    while q:
        (r, c) = q.pop_smallest()
        discovers[r][c] = 1
        for (adj_r, adj_c) in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
            if 0 > adj_r or adj_r > 17 or 0 > adj_c or adj_c > 12:
                continue

            estimated_cost = distances_from_start[r][c] + \
                distances_to_goal[adj_r][adj_c] + \
                turning_cost(before[r][c], (r, c), (adj_r, adj_c))
            if (is_valid_move(graph, adj_r, adj_c) and
                    discovers[adj_r][adj_c] != 1 and
                    cost[adj_r][adj_c] > estimated_cost):
                distances_from_start[adj_r][adj_c] = distances_from_start[r][c] + \
                    turning_cost(before[r][c], (r, c), (adj_r, adj_c))
                cost[adj_r][adj_c] = estimated_cost
                q.__setitem__((adj_r, adj_c), estimated_cost)
                before[adj_r][adj_c] = (r, c)

    (trace_r, trace_c) = bounded_goal_point
    while (trace_r, trace_c) != bounded_start_point:
        results.append((trace_r + 1, trace_c + 1))
        try:
            (trace_r, trace_c) = before[trace_r][trace_c]
        except TypeError:
            return False

    return results[::-1]


def get_shortest_path_moves(robot, start, goal, before_start_point=None, is_give_up=False):
    limited_map = []
    if is_give_up:
        for row in robot.discovered_map:
            limited_map.append([1 if x == 2 else x for x in row])
    else:
        limited_map = robot.discovered_map

    if limited_map[start[0]][start[1]]:
        return False

    cells = find_fastest_path(graph=limited_map, start_point=start, goal_point=goal,
                              before_start_point=before_start_point)

    prev_cell = (start[0], start[1])

    move_list = []

    potential_facing = robot.facing
    potential_center = start

    if not cells:
        return False

    for cell in cells:
        y_diff = cell[0] - prev_cell[0]

        if y_diff == -1:
            abs_dir = SOUTH
        elif y_diff == 1:
            abs_dir = NORTH
        elif y_diff == 0:
            x_diff = cell[1] - prev_cell[1]
            if x_diff == -1:
                abs_dir = WEST
            elif x_diff == 1:
                abs_dir = EAST
        to_move = abs_dir - potential_facing

        if to_move == -3:
            to_move = RIGHT
        elif to_move == -2:
            to_move = BACKWARD
        elif to_move == 3:
            to_move = LEFT

        potential_facing = (potential_facing + to_move) % 4

        if potential_facing == NORTH:
            potential_center = get_coordinates(get_grid_index(potential_center[0], potential_center[1]) + 15)
        elif potential_facing == EAST:
            potential_center = get_coordinates(get_grid_index(potential_center[0], potential_center[1]) + 1)
        elif potential_facing == SOUTH:
            potential_center = get_coordinates(get_grid_index(potential_center[0], potential_center[1]) - 15)
        elif potential_facing == WEST:
            potential_center = get_coordinates(get_grid_index(potential_center[0], potential_center[1]) - 1)

        move_list.append(to_move)

        prev_cell = cell

    return move_list


def get_shortest_valid_path(robot, start_cell, goal_cells):
    center_y, center_x = get_coordinates(start_cell)
    for target in goal_cells:
        target_y, target_x = get_coordinates(target)
        moves = get_shortest_path_moves(robot, (center_y, center_x), (target_y, target_x))
        if moves:
            return moves
    return moves
