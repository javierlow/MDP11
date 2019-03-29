import re
from tkinter.filedialog import askopenfilename
import threading
from ast import literal_eval
from time import time, sleep

from exploration import Exploration
from fastest_path import *
from connection_client import Sender


class Controller:
    def __init__(self, sim):
        self._is_sim = sim

        if self._is_sim:
            print('sim run')
            import tkinter as tk
            import GUI
            root = tk.Tk()
            self._gui = GUI.Window(root)
            self._gui.mainloop()
            from simulator import Robot
            self._robot = Robot(exploration_status=[[0] * 15 for _ in range(20)],
                                facing=NORTH,
                                discovered_map=[[2] * 15 for _ in range(20)],
                                real_map=[[]])
        else:
            print('real run')
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
        elif msg == "au":
            self._auto_update = True
        elif msg == "mu":
            self._auto_update = False
            self._update_android(True, True, override=True)
        elif msg[0:8] == "waypoint":
            self._set_way_point(msg[9:])
        elif msg == "bf":
            thread = threading.Thread(target=self._move_fastest_path)
            thread.daemon = True
            thread.start()
        elif msg == "st":
            sleep(0.05)
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

    def _set_way_point(self, coordinate):
        (col, row) = literal_eval(coordinate)
        self._way_point = (row, col)

    def _calibrate(self):
        if not self._is_sim:
            self._sender.send_android('{"status":"calibrating"}')
            self._sender.send_arduino('z')
            self._sender.wait_arduino('D')
            self._robot.turn_robot(self._sender, RIGHT)
            self._robot.get_sensor_readings(self._sender)
            self._robot.turn_robot(self._sender, LEFT)
            self._sender.send_arduino('z')
            self._sender.wait_arduino('D')
        self._sender.send_android('{"status":"calibrating done"}')

    def _update_map_android(self):
        self._sender.send_android('{"exploreMap":"%s"}' % self._robot.get_explore_string())
        self._sender.send_android('{"obstacleMap":"%s"}' % self._robot.get_map_string())

    def _update_coords_android(self):
        y, x = get_coordinates(self._robot.center)
        self._sender.send_android('{"robotPosition":[%s,%s,%s]}' % (str(x), str(y), str(self._robot.facing)))

    def _update_android(self, is_update_map, is_update_coords, override=False):
        if self._auto_update or override:
            if is_update_map:
                self._update_map_android()
            if is_update_coords:
                self._update_coords_android()

    def _explore(self):
        start_time = time()

        exploration = Exploration(self._robot, start_time, self._explore_limit, self._time_limit)

        if self._is_sim:
            run = exploration.start_real_simulation()
        else:
            run = exploration.start_real(self._sender)

        next(run)
        self._update_android(True, True)
        while True:
            try:
                # Exploration until completion

                while True:
                    run.send(0)
                    self._update_android(True, True)

                    run.send(0)
                    if self._is_sim:
                        sleep(1)

                    self._update_android(True, True)

                    is_complete = run.send(0)
                    if is_complete:
                        break

                    is_looped = run.send(0)
                    if is_looped:
                        while True:
                            updated_or_moved, value, is_complete = run.send(0)
                            if self._is_sim:
                                sleep(1)
                            if updated_or_moved == "updated" or updated_or_moved == "moved":
                                self._update_android(True, True)
                                if updated_or_moved == "updated":
                                    self._gui.update_cells(value)
                                elif updated_or_moved == "moved":
                                    self._gui.move_robot(value)
                            else:
                                break

                            if is_complete:
                                break
                        break

                # Returning to start after completion
                while True:
                    run.send(0)
                    if self._is_sim:
                        sleep(1)

                    self._update_android(True, True)

            except StopIteration:
                if not self._is_sim:
                    enable_print()
                    print('EXPLORE_STR:', self._robot.get_explore_string())
                    print('MAP_STR:', self._robot.get_map_string())
                    disable_print()
                    print('Returned to start!')
                    self._sender.send_arduino('j')
                    self._sender.wait_arduino('U')
                    if self._robot.facing == WEST:
                        print('ENTERED FACING WEST')
                        sleep(0.05)
                        self._robot.turn_robot(self._sender, LEFT)
                        self._sender.send_arduino('j')
                        self._sender.wait_arduino('U')
                        self._robot.turn_robot(self._sender, RIGHT)
                        sleep(0.05)
                        self._robot.turn_robot(self._sender, RIGHT)
                        sleep(0.05)
                        self._sender.send_arduino('x')
                        self._sender.wait_arduino('D')
                    elif self._robot.facing == SOUTH:
                        print('ENTERED FACING SOUTH')
                        sleep(0.05)
                        self._robot.turn_robot(self._sender, RIGHT)
                        self._sender.send_arduino('j')
                        self._sender.wait_arduino('U')
                        sleep(0.05)
                        self._robot.turn_robot(self._sender, RIGHT)
                        sleep(0.05)
                        self._sender.send_arduino('x')
                        self._sender.wait_arduino('D')
                break

        print('Calibrating...')
        self._calibrate_after_exploration()

    def _calibrate_after_exploration(self):
        self._fastest_path = self._find_fastest_path()

        if self._is_sim:
            sleep(1)
            self._robot.turn_robot(self._fastest_path[0])
        else:
            self._robot.turn_robot(self._sender, self._fastest_path[0])
        self._fastest_path[0] = FORWARD
        self._update_android(True, True)
        self._sender.send_android('{"status":"explore done"}')
        self._sender.send_android('{"status":"calibrating done"}')

    def _find_fastest_path(self):
        """Calculate and return the set of moves required for the fastest path."""
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
            if self._is_sim:
                for move in self._fastest_path:
                    if self._is_sim:
                        sleep(1)

                    self._robot.move_robot(move)
                    self._update_android(True, True)
            else:
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
                        self._sender.wait_arduino('M')
        else:
            print("No valid path")
