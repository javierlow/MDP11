import re
from tkinter.filedialog import askopenfilename
import threading
from ast import literal_eval
from time import time, sleep

from exploration import Exploration
from fastest_path import *
from connection_client import Sender


class Controller:
    def __init__(self):
        print('real run')
        self._last_calibrate = 0
        self._explore_limit = 100.0
        self._time_limit = 720
        from robot import Robot
        self._robot = Robot(exploration_status=[[0] * 15 for _ in range(20)],
                            facing=NORTH,
                            discovered_map=[[2] * 15 for _ in range(20)])
        self._sender = Sender(self._msg_handler)
        self._auto_update = True
        enable_print()
        print('init complete!')
        disable_print()
        try:
            import winsound
            frequency = 2500
            duration = 250
            winsound.Beep(frequency, duration)
            winsound.Beep(frequency, duration)
        except ImportError:
            enable_print()
            print('beep')
            disable_print()

    def _msg_handler(self, msg):
        if msg == "ca":
            thread = threading.Thread(target=self._calibrate)
            thread.daemon = True
            thread.start()
        elif msg == "be":
            thread = threading.Thread(target=self._explore)
            thread.daemon = True
            thread.start()
        elif msg[0:8] == "waypoint":
            self._set_way_point(msg[8:])
        elif msg == "bf":
            thread = threading.Thread(target=self._move_fastest_path)
            thread.daemon = True
            thread.start()
        elif msg == "st":
            raise StopIteration
        elif msg == "w":
            self._sender.send_arduino('w')
        elif msg == "a":
            self._sender.send_arduino('a')
        elif msg == "d":
            self._sender.send_arduino('d')
        elif msg == "s":
            self._sender.send_arduino('s')
        elif msg == "o":
            self._sender.send_arduino('g')

    def _load_map(self):
        filename = askopenfilename(title="Select Map Descriptor", filetypes=[("Text Files (*.txt)", "*.txt")])

        if filename:
            print(filename)
            if self._parse_map(filename):
                return True
            print("File %s cannot be parsed" % filename)
            return False
        print("File %s does not exist" % filename)
        return False

    def _parse_map(self, filename):
        file = open(filename, mode="r")
        map_str = file.read()

        match = re.fullmatch("[01\n]*", map_str)
        if match:
            self._grid_map = []
            row_strings = map_str.split("\n")
            for row_string in row_strings:
                grid_row = []
                for char in row_string:
                    bit = int(char)
                    grid_row.append(bit)
                self._grid_map.append(grid_row)
            return True

        return False

    def _set_way_point(self, coordinate):
        (col, row) = literal_eval(coordinate)
        self._way_point = (row, col)

    def _calibrate(self):
        self._sender.send_arduino('f')
        self._sender.wait_arduino('D')

    def _update_android(self, override=True):
        if self._auto_update or override:
            y, x = get_coordinates(self._robot.center)
            direction = get_direction_str(self._robot.facing)
            mdf = 'MDF|%s|%s|%s|%s|%s' % (str(y), str(x), direction, self._robot.get_explore_string(),
                                          self._robot.get_map_string())
            enable_print()
            print('(%d,%d)' % (y, x))
            self._sender.send_android(mdf)

    def _explore(self):
        start_time = time()
        exploration = Exploration(self._robot, start_time, self._explore_limit, self._time_limit)

        run = exploration.start_real_efficient(self._sender)

        next(run)
        self._update_android()
        while True:
            try:
                # Exploration until completion

                while True:
                    run.send(0)
                    self._update_android()

                    run.send(0)

                    self._update_android()

                    is_complete = run.send(0)
                    if is_complete:
                        break

                    is_looped = run.send(0)
                    if is_looped:
                        while True:
                            updated_or_moved, value, is_complete = run.send(0)
                            if updated_or_moved == "updated" or updated_or_moved == "moved":
                                self._update_android()
                                self._last_calibrate = self._last_calibrate + 1
                                if self._last_calibrate >= 7:
                                    y, x = get_coordinates(self._robot.center)
                                    enable_print()
                                    print('(%d,%d)' % (x, y))
                                    if y >= 17 and x <= 2:
                                        self._sender.send_arduino('r')
                                        self._last_calibrate = 0
                                        enable_print()
                                        print('top left corner calibrate')
                                        disable_print()
                                    elif y >= 17 and x >= 12:
                                        self._sender.send_arduino('r')
                                        self._last_calibrate = 0
                                        enable_print()
                                        print('goal zone calibrate')
                                        disable_print()
                                    elif y <= 2 and x >= 12:
                                        self._sender.send_arduino('r')
                                        self._last_calibrate = 0
                                        enable_print()
                                        print('bottom left corner calibrate')
                                        disable_print()
                                    elif x <= 2 or x >= 12:
                                        self._sender.send_arduino('e')
                                        self._last_calibrate = 0
                                        enable_print()
                                        print('wall calibrate (x)')
                                        disable_print()
                                    elif y <= 2 or y >= 17:
                                        self._sender.send_arduino('e')
                                        self._last_calibrate = 0
                                        enable_print()
                                        print('wall calibrate (y)')
                                        disable_print()
                            else:
                                break

                            if is_complete:
                                break
                        break

                # Returning to start after completion
                while True:
                    run.send(0)
                    self._update_android()

            except StopIteration:
                enable_print()
                print('EXPLORE_STR:', self._robot.get_explore_string())
                print('MAP_STR:', self._robot.get_map_string())
                disable_print()
                print('Returned to start!')
                if self._robot.facing == WEST:
                    print('ENTERED FACING WEST')
                    self._robot.turn_robot(self._sender, LEFT)
                    self._calibrate()
                elif self._robot.facing == SOUTH:
                    print('ENTERED FACING SOUTH')
                    self._sender.send_arduino('c')
                    self._calibrate()
                break

        print('Calibrating...')
        self._calibrate_after_exploration()

    def _calibrate_after_exploration(self):
        self._fastest_path = self._find_fastest_path()
        self._robot.turn_robot(self._sender, self._fastest_path[0])
        self._fastest_path[0] = FORWARD
        self._update_android()
        self._sender.send_android('endExplore')

    def _find_fastest_path(self):
        from simulator import Robot
        clone_robot = Robot(exploration_status=self._robot.exploration_status,
                            facing=self._robot.facing,
                            discovered_map=self._robot.discovered_map,
                            real_map=[[0] * 15 for _ in range(20)])

        fastest_path_start_way_point = get_shortest_path_moves(clone_robot,
                                                               start=(1, 1),
                                                               goal=self._way_point)

        if fastest_path_start_way_point:
            for move in fastest_path_start_way_point:
                clone_robot.move_robot(move)

        before_way_point = previous_cell(clone_robot.center, clone_robot.facing)

        fastest_path_way_point_goal = get_shortest_path_moves(clone_robot,
                                                              start=self._way_point,
                                                              goal=(18, 13),
                                                              before_start_point=before_way_point)

        return fastest_path_start_way_point + fastest_path_way_point_goal

    def _move_fastest_path(self):
        if self._fastest_path:
            move_str = get_fastest_path_move_string(self._fastest_path)
            moves = move_str.split('/')
            for move in moves:
                move_len = len(move)
                if move[0] == 'n':
                    move = move[:-1] + 't'
                elif move[0] == 'a' or move[0] == 'd':
                    pass
                self._sender.send_arduino(move)
                for i in range(move_len):
                    self._sender.wait_arduino('D')
            self._sender.send_android('endFastest')
        else:
            print("No valid path")
