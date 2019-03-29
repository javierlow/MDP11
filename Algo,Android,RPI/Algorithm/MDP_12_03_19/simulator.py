from time import time
from utils import *


class Robot:
    def __init__(self, exploration_status, facing, discovered_map, real_map):
        self.exploration_status = exploration_status
        self.center = 17
        self.facing = facing
        self.discovered_map = discovered_map
        self.real_map = real_map
        self._sensors = [
            {"mount_loc": SWS, "facing": WEST, "range": 4, "blind_spot": 0},
            {"mount_loc": NWS, "facing": WEST, "range": 4, "blind_spot": 0},
            {"mount_loc": NWS, "facing": NORTH, "range": 4, "blind_spot": 0},
            {"mount_loc": NS, "facing": NORTH, "range": 4, "blind_spot": 0},
            {"mount_loc": NES, "facing": NORTH, "range": 4, "blind_spot": 0},
            {"mount_loc": NES, "facing": EAST, "range": 5, "blind_spot": 0}
        ]

    def _mark_explored(self, y_or_cell, x=None):
        if x is None:
            y_or_cell, x = get_coordinates(y_or_cell)

        if x < 0 or y_or_cell < 0:
            raise IndexError

        if not self.exploration_status[y_or_cell][x]:
            self.exploration_status[y_or_cell][x] = 1
            self.discovered_map[y_or_cell][x] = self.real_map[y_or_cell][x]
            return get_grid_index(y_or_cell, x), self.discovered_map[y_or_cell][x]
        return None, None

    def in_efficiency_limit(self):
        if (self.center in range(257, 270) and self.facing == EAST) \
                or (self.center in range(28, 284, 15) and self.facing == SOUTH) \
                or (self.center in range(32, 45) and self.facing == WEST) \
                or (self.center in range(18, 274, 15) and self.facing == NORTH):
            return True

        return False

    def mark_robot_standing(self):
        robot_cells = get_robot_cells(self.center)
        updated_cells = {}
        for cell in robot_cells:
            updated_cell, value = self._mark_explored(cell)
            if updated_cell is not None:
                updated_cells[updated_cell] = value

        return updated_cells

    def get_completion_percentage(self):
        count = 0
        for row in self.exploration_status:
            for i in row:
                count += i

        return float(count) / 3.0

    def is_complete(self, explore_limit, start_time, time_limit):
        return self.get_completion_percentage() >= float(explore_limit) \
            or float(time() - start_time >= time_limit)

    def turn_robot(self, direction):
        self.facing = (self.facing + direction) % 4

    def move_robot(self, direction):
        self.turn_robot(direction)

        if self.facing == NORTH:
            self.center += 15
        elif self.facing == EAST:
            self.center += 1
        elif self.facing == SOUTH:
            self.center -= 15
        elif self.facing == WEST:
            self.center -= 1

        updated_cells = self.mark_robot_standing()

        return updated_cells

    def check_free(self, direction):
        true_bearing = (self.facing + direction) % 4

        robot_cells = get_robot_cells(self.center)

        try:
            if true_bearing == NORTH:
                y, x = get_coordinates(robot_cells[0])
                y += 1
                if y < 0 or x < 0:
                    raise IndexError
                return not (self.discovered_map[y][x] == 1 or self.discovered_map[y][x + 1] == 1
                            or self.discovered_map[y][x + 2] == 1)
            elif true_bearing == EAST:
                y, x = get_coordinates(robot_cells[2])
                x += 1
                if y < 2 or x < 0:
                    raise IndexError
                return not (self.discovered_map[y][x] == 1 or self.discovered_map[y - 1][x] == 1
                            or self.discovered_map[y - 2][x] == 1)
            elif true_bearing == SOUTH:
                y, x = get_coordinates(robot_cells[6])
                y -= 1
                if y < 0 or x < 0:
                    raise IndexError
                return not (self.discovered_map[y][x] == 1 or self.discovered_map[y][x + 1] == 1
                            or self.discovered_map[y][x + 2] == 1)
            elif true_bearing == WEST:
                y, x = get_coordinates(robot_cells[0])
                x -= 1
                if y < 2 or x < 0:
                    raise IndexError
                return not (self.discovered_map[y][x] == 1 or self.discovered_map[y - 1][x] == 1
                            or self.discovered_map[y - 2][x] == 1)
        except IndexError:
            return False

    def get_sensor_readings(self):
        updated_cells = {}

        for sensor in self._sensors:
            true_facing = (sensor["facing"] + self.facing) % 4

            if sensor["mount_loc"] != CS:
                offset = self.facing * 2
                true_mounting = (sensor["mount_loc"] + offset) % 8
            else:
                true_mounting = CS

            robot_cells = get_robot_cells(self.center)

            try:
                if true_mounting == NWS:
                    origin = robot_cells[0]
                elif true_mounting == NS:
                    origin = robot_cells[1]
                elif true_mounting == NES:
                    origin = robot_cells[2]
                elif true_mounting == WS:
                    origin = robot_cells[3]
                elif true_mounting == ES:
                    origin = robot_cells[5]
                elif true_mounting == SWS:
                    origin = robot_cells[6]
                elif true_mounting == SS:
                    origin = robot_cells[7]
                elif true_mounting == SES:
                    origin = robot_cells[8]
                elif true_mounting == CS:
                    origin = robot_cells[4]

                y, x = get_coordinates(origin)
                read_range = list(range(sensor["blind_spot"] + 1, sensor["range"] + 1))

                for cell in read_range:
                    if true_facing == NORTH:
                        to_explore = (y + cell, x)
                    elif true_facing == EAST:
                        to_explore = (y, x + cell)
                    elif true_facing == SOUTH:
                        to_explore = (y - cell, x)
                    elif true_facing == WEST:
                        to_explore = (y, x - cell)

                    updated_cell, value = self._mark_explored(to_explore[0], to_explore[1])
                    if updated_cell is not None:
                        updated_cells[updated_cell] = value

                    if self.discovered_map[to_explore[0]][to_explore[1]] == 1:
                        raise IndexError

            except IndexError:
                continue
        print(updated_cells)
        return updated_cells

    def get_explore_string(self):
        exploration_status = self.exploration_status[:]

        explore_str = ''.join(str(grid) for row in exploration_status for grid in row)

        explore_status_string = '11%s11' % explore_str
        explore_status_string = str(hex(int(explore_status_string, 2)))

        file = open("explore_string.txt", "w+")
        file.write(explore_status_string[2:])
        file.close()

        return explore_status_string[2:]

    def get_map_string(self):
        discovered_map = self.discovered_map[:]

        map_str = ''.join(str(grid) for row in discovered_map for grid in row if grid != 2)
        pad_length = (8 - (len(map_str) % 8)) % 8
        pad = '0' * pad_length
        map_string = '1111%s%s' % (map_str, pad)
        map_string = str(hex(int(map_string, 2)))

        map_string = map_string[3:]

        file = open("map_string.txt", "w+")
        file.write(map_string)
        file.close()

        return map_string
