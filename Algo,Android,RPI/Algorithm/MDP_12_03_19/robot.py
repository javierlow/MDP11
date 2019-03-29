import re
from utils import *
from time import time, sleep


class Robot:
    def __init__(self, exploration_status, facing, discovered_map):
        self.exploration_status = exploration_status
        self.center = 17
        self.facing = facing
        self.discovered_map = discovered_map
        self._probability_map = [[[0.0, 0.0] for _ in range(15)] for _ in range(20)]
        self._arrow_map = [[[0, 0, 0, 0] for _ in range(15)] for _ in range(20)]
        self._sensors = [
            {"mount_loc": SWS, "facing": WEST, "range": 4, "blind_spot": 0},
            {"mount_loc": NWS, "facing": WEST, "range": 4, "blind_spot": 0},
            {"mount_loc": NWS, "facing": NORTH, "range": 4, "blind_spot": 0},
            {"mount_loc": NS, "facing": NORTH, "range": 4, "blind_spot": 0},
            {"mount_loc": NES, "facing": NORTH, "range": 4, "blind_spot": 0},
            {"mount_loc": NS, "facing": EAST, "range": 5, "blind_spot": 0}
        ]

        self.num_sensor_readings = 11
        regex_str = '^(\d,){%s}$' % (len(self._sensors) * self.num_sensor_readings)
        self._readings_regex = re.compile(regex_str)

    def _mark_probability(self, cell, count, total):
        y, x = get_coordinates(cell)
        print(y, x, count, total)

        if self._probability_map[y][x][0] == 1.0 and self._probability_map[y][x][1] == 0.0:
            print('perm')
            return

        self._probability_map[y][x][0] += count
        self._probability_map[y][x][1] += total

        prob_obstacle = self._probability_map[y][x][0]
        prob_total = self._probability_map[y][x][1]

        print(y, x, prob_obstacle, prob_total)

        if not self.exploration_status[y][x]:
            self.exploration_status[y][x] = 1

        if prob_obstacle / prob_total > 0.5:
            self.discovered_map[y][x] = 1
            return 1
        else:
            self.discovered_map[y][x] = 0
            return 0

    def _mark_permanent(self, cell):
        y, x = get_coordinates(cell)

        self._probability_map[y][x][0] = 1.0
        self._probability_map[y][x][1] = 0.0

        if not self.exploration_status[y][x]:
            self.exploration_status[y][x] = 1

        self.discovered_map[y][x] = 0

        return True

    def _mark_arrow_taken(self, y, x, facing):
        opposite = (facing + 2) % 4

        self._arrow_map[y][x][facing] = 1
        self._arrow_map[y][x][opposite] = 1

        return True

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
        mark_permanent = self._mark_permanent
        for cell in robot_cells:
            if mark_permanent(cell):
                updated_cells[cell] = 0

        return updated_cells

    def get_completion_percentage(self):
        count = 0.0
        for row in self.exploration_status:
            for i in row:
                count += i

        return count / 3.0

    def is_complete(self, explore_limit, start_time, time_limit):
        completion = self.get_completion_percentage
        return completion() >= explore_limit \
            or float(time() - start_time >= time_limit)

    def turn_robot(self, sender, direction):
        if direction == FORWARD:
            return

        if direction == BACKWARD:
            sender.send_arduino(get_arduino_cmd(LEFT))
            self.facing = (self.facing + LEFT) % 4
            direction = LEFT
            sender.wait_arduino('D')

        sender.send_arduino(get_arduino_cmd(direction))
        self.facing = (self.facing + direction) % 4

        sender.wait_arduino('D')

        if ARROW_SCAN:
            self.check_arrow(sender)

    def move_robot(self, sender, direction):
        self.turn_robot(sender, direction)

        sender.send_arduino(get_arduino_cmd(FORWARD))

        if self.facing == NORTH:
            self.center += 15
        elif self.facing == EAST:
            self.center += 1
        elif self.facing == SOUTH:
            self.center -= 15
        elif self.facing == WEST:
            self.center -= 1

        updated_cells = self.mark_robot_standing()

        sender.wait_arduino('D')

        if ARROW_SCAN:
            self.check_arrow(sender)

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

    def is_arrow_possible(self):
        arrow_range = 1
        y, x = get_coordinates(self.center)
        discovered_map = self.discovered_map
        arrow_map = self._arrow_map
        facing = self.facing

        try:
            for distance in range(2, arrow_range + 2):
                if facing == NORTH:
                    new_x = x - distance
                    if new_x < 0:
                        raise IndexError
                    print('checking %s,%s %s,%s %s,%s' % (y, new_x, y + 1, new_x, y - 1, new_x))
                    obstacles = [discovered_map[y][new_x] == 1, discovered_map[y + 1][new_x] == 1,
                                 discovered_map[y - 1][new_x] == 1]
                    marked = [arrow_map[y][new_x][facing], arrow_map[y + 1][new_x][facing],
                              arrow_map[y][new_x][facing]]
                    if any(obstacles) and not any(marked):
                        self._mark_arrow_taken(y, new_x, facing)
                        self._mark_arrow_taken(y + 1, new_x, facing)
                        self._mark_arrow_taken(y - 1, new_x, facing)
                        return True
                elif facing == EAST:
                    new_y = y + distance
                    print('checking %s,%s %s,%s %s,%s' % (new_y, x, new_y, x + 1, new_y, x - 1))
                    obstacles = [discovered_map[new_y][x] == 1, discovered_map[new_y][x + 1] == 1,
                                 discovered_map[new_y][x - 1] == 1]
                    marked = [arrow_map[new_y][x][facing], arrow_map[new_y][x + 1][facing],
                              arrow_map[new_y][x - 1][facing]]
                    if any(obstacles) and not any(marked):
                        self._mark_arrow_taken(new_y, x, facing)
                        self._mark_arrow_taken(new_y, x + 1, facing)
                        self._mark_arrow_taken(new_y, x - 1, facing)
                        return True
                elif facing == SOUTH:
                    new_x = x + distance
                    print('checking %s,%s %s,%s %s,%s' % (y, new_x, y + 1, new_x, y - 1, new_x))
                    obstacles = [discovered_map[y][new_x] == 1, discovered_map[y + 1][new_x] == 1,
                                 discovered_map[y - 1][new_x] == 1]
                    marked = [arrow_map[y][new_x][facing], arrow_map[y + 1][new_x][facing],
                              arrow_map[y][new_x][facing]]
                    if any(obstacles) and not any(marked):
                        self._mark_arrow_taken(y, new_x, facing)
                        self._mark_arrow_taken(y + 1, new_x, facing)
                        self._mark_arrow_taken(y - 1, new_x, facing)
                        return True
                elif facing == WEST:
                    new_y = y - distance
                    if new_y < 0:
                        raise IndexError
                    print('checking %s,%s %s,%s %s,%s' % (new_y, x, new_y, x + 1, new_y, x - 1))
                    obstacles = [discovered_map[new_y][x] == 1, discovered_map[new_y][x + 1] == 1,
                                 discovered_map[new_y][x - 1] == 1]
                    marked = [arrow_map[new_y][x][facing], arrow_map[new_y][x + 1][facing],
                              arrow_map[new_y][x - 1][facing]]
                    if any(obstacles) and not any(marked):
                        self._mark_arrow_taken(new_y, x, facing)
                        self._mark_arrow_taken(new_y, x + 1, facing)
                        self._mark_arrow_taken(new_y, x - 1, facing)
                        return True
            return False
        except IndexError:
            return False

    def check_arrow(self, sender):
        if self.is_arrow_possible():
            y, x = get_coordinates(self.center)
            msg = '%s,%s,%s' % (x, y, self.facing)
            enable_print()
            sender.send_rpi(msg)
            sender.wait_rpi('Y')
            disable_print()

        else:
            print(get_coordinates(self.center), 'false')

    def get_sensor_readings(self, sender):
        mark_probability = self._mark_probability

        sender.send_arduino('g')
        readings = sender.wait_arduino(self._readings_regex, sensor_reading=True)
        print('Readings: %s' % readings)
        readings = readings.split(',')

        readings = [int(x) for x in readings]

        readings = [readings[i:i + len(self._sensors)] for i in range(0, len(readings), len(self._sensors))]

        readings = [[row[i] for row in readings] for i, _ in enumerate(readings[0])]
        print(readings)
        robot_cells = get_robot_cells(self.center)
        sensors = self._sensors[:]
        sensor_index = sensors.index
        updated_cells = {}

        for sensor in sensors:
            true_facing = (sensor["facing"] + self.facing) % 4

            offset = self.facing * 2
            true_mounting = (sensor["mount_loc"] + offset) % 8
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

            reading = readings[sensor_index(sensor)]
            print('Sensor', sensor_index(sensor))

            weight = 4
            for cell in read_range:
                try:
                    if true_facing == NORTH:
                        to_explore = (y + cell, x)
                    elif true_facing == EAST:
                        to_explore = (y, x + cell)
                    elif true_facing == SOUTH:
                        to_explore = (y - cell, x)
                    elif true_facing == WEST:
                        to_explore = (y, x - cell)

                    if to_explore[0] < 0 or to_explore[1] < 0:
                        print('ie')
                        raise IndexError

                    cell_index = get_grid_index(to_explore[0], to_explore[1])

                    if mark_probability(cell_index, weight * reading.count(cell), weight * self.num_sensor_readings):
                        raise IndexError

                    weight /= 2

                except IndexError:
                    break
            print('br')

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
