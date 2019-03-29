import sys
import os
from constants import *


def get_coordinates(cell):
    x = (cell - 1) % 15
    y = (cell - 1) // 15

    return y, x


def get_grid_index(y, x):
    if y not in range(20) or x not in range(15):
        raise IndexError

    return (y * 15) + x + 1


def get_robot_cells(cell):
    cells = [cell + 14, cell + 15, cell + 16,
             cell - 1, cell, cell + 1,
             cell - 16, cell - 15, cell - 14]

    return cells


def previous_cell(cell, facing):
    y, x = get_coordinates(cell)
    if facing == 0:
        return y - 1, x
    elif facing == 1:
        return y, x - 1
    elif facing == 2:
        return y + 1, x
    elif facing == 3:
        return y, x + 1
    return None


def get_arduino_cmd(direction):
    if direction == FORWARD:
        return 'w'
    if direction == LEFT:
        return 'a'
    if direction == BACKWARD:
        return 's'
    if direction == RIGHT:
        return 'd'


def get_fastest_path_move_string(fastest_path, for_exploration=False):
    move_str = ''
    for move in fastest_path:
        if move == RIGHT or move == BACKWARD or move == LEFT:
            move_str += '/'
            move_str += get_arduino_cmd(move)
            move_str += '/'

        if for_exploration:
            move_str += get_arduino_cmd(FORWARD)
        else:
            move_str += 'n'

    return move_str


def get_direction_str(direction):
    if direction == 0:
        return 'NORTH'
    elif direction == 1:
        return 'EAST'
    elif direction == 2:
        return 'SOUTH'
    elif direction == 3:
        return 'WEST'


def disable_print():
    if not DEBUG_MODE:
        sys.stdout = open(os.devnull, 'w')


def enable_print():
    if not DEBUG_MODE:
        sys.stdout = sys.__stdout__
