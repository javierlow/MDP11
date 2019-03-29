import fastest_path as fp
from tkinter import *
from tkinter.filedialog import askopenfilename
from time import time, sleep
from simulator import Robot
from exploration import Exploration
from utils import *
from controller_with_sim import SimController
from robot import Robot as RealRobot
import threading
from connection_client import Sender


class TimeUp(Exception):
    def __init__(self):
        print("TIME'S UP (GUI)")


class Window(Frame):

    _grid_size = 30

    def __init__(self, master):

        Frame.__init__(self, master)

        self._real_robot = RealRobot(exploration_status=[[0] * 15 for _ in range(20)],
                            facing=NORTH,
                            discovered_map=[[2] * 15 for _ in range(20)])
        self._sender = Sender(self._msg_handler)
        self._auto_update = True

        self._master = master
        print("init window starting")
        self._init_window()
        print("init window completed")
        self._is_real_run = False

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

    def _init_window(self):

        self._master.title("Physical Robot Simulation")

        self.pack(fill=BOTH, expand=1)

        bg_frame = Frame(self)
        bg_frame.pack(fill=X, padx=90)

        self._time_step_label = Label(bg_frame, text="time_step(seconds):")
        self._time_step_label.grid(row=0, column=0)

        self._time_step_entry = Entry(bg_frame, width=5, justify='center')
        self._time_step_entry.insert(END, "0.1")
        self._time_step_entry.grid(row=0, column=1)

        self._explore_label = Label(bg_frame, text="Explore Cutoff:")
        self._explore_label.grid(row=1, column=0)

        self._explore_entry = Entry(bg_frame, width=5, justify='center')
        self._explore_entry.insert(END, "100")
        self._explore_entry.grid(row=1, column=1)

        self._percentage_completion_label = Label(bg_frame, text="0.0%")
        self._percentage_completion_label.grid(row=1, column=2)

        self._time_limit_label = Label(bg_frame, text="Time Limit(seconds):")
        self._time_limit_label.grid(row=2, column=0)

        self._time_limit_entry = Entry(bg_frame, width=5, justify='center')
        self._time_limit_entry.insert(END, "30")
        self._time_limit_entry.grid(row=2, column=1)

        self._time_spent_label = Label(bg_frame, text="0.0s")
        self._time_spent_label.grid(row=2, column=2)

        self._button = Button(bg_frame, text="Restart", command=self._restart)
        self._button.grid(row=3, column=0)

        self._button = Button(bg_frame, text="Connect", command=self._connect)
        self._button.grid(row=3, column=1)

        self._loadBtn = Button(bg_frame, text="Load Map", command=self._load_map)
        self._loadBtn.grid(row=3, column=2)

        self._button = Button(bg_frame, text="Explore", command=self._explore)
        self._button.grid(row=3, column=3)

        self._fp_button = Button(bg_frame, text="Find Fastest Path", command=self._find_fastest_path)
        self._fp_button.grid(row=3, column=4)

        self._canvas = Canvas(self, height=20 * self._grid_size + 1, width=15 * self._grid_size + 1,
                              borderwidth=0, highlightthickness=0, background='#ffffff')
        self._canvas.pack(padx=20, pady=20)

        # Draw grid
        self._draw_grid()

        # Draw robot
        self._facing = NORTH
        self._draw_robot(17, self._facing)

        self._robot = Robot(exploration_status=[[0] * 15 for _ in range(20)],
                            facing=EAST,
                            discovered_map=[[2] * 15 for _ in range(20)],
                            real_map=[[]])

    def _update_android(self, override=True):
        if self._auto_update or override:
            y, x = get_coordinates(self._robot.center)
            direction = get_direction_str(self._robot.facing)
            mdf = 'MDF|%s|%s|%s|%s|%s' % (str(y), str(x), direction, self._robot.get_explore_string(),
                                          self._robot.get_map_string())
            print('(%d,%d)' % (y, x))
            self._sender.send_android(mdf)

    def _connect(self):
        self._controller = SimController(self._master)
        self._is_real_run = True
        # self._sender.send_arduino('be')

    def _restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def _draw_grid(self):
        self._grid_squares = []

        for y in range(20):
            temp_row = []
            for x in range(15):
                temp_square = self._canvas.create_rectangle(x * self._grid_size, (20 - 1 - y) * self._grid_size,
                                                            (x + 1) * self._grid_size,
                                                            (20 - y) * self._grid_size, width=3)

                self._canvas.tag_bind(temp_square, "<Button-1>",
                                      lambda event, arg=temp_square: self._on_grid_click(event, arg))
                temp_row.append(temp_square)

            self._grid_squares.append(temp_row)

    def _draw_robot(self, location, facing):

        if location in range(286, 301) or location in range(1, 16) \
                or location in range(15, 300, 15) or location in range(1, 286, 15):
            print("invalid location")
            return

        top_left_grid = self._canvas.coords(location + 15 - 1)
        x = top_left_grid[0]
        y = top_left_grid[1]

        self._robot_graphic = self._canvas.create_oval(x, y, x + (3 * self._grid_size), y + (3 * self._grid_size),
                                                       width=2, fill="#336666", outline="#252a33")
        self._draw_head(location, facing)

    def _draw_head(self, location, facing):

        if facing == NORTH:
            corner = self._canvas.coords(location + 15)
        elif facing == SOUTH:
            corner = self._canvas.coords(location - 15)
        elif facing == EAST:
            corner = self._canvas.coords(location + 1)
        else:
            corner = self._canvas.coords(location - 1)
        x, y = corner[0], corner[1]
        self._head = self._canvas.create_oval(x + (self._grid_size // 3), y + (self._grid_size // 3),
                                              x + (2 * (self._grid_size // 3)) + 1,
                                              y + (2 * (self._grid_size // 3)) + 1,
                                              width=0, fill="#c3c3c3")

    def _turn_head(self, facing, direction):
        if facing == NORTH:
            if direction == LEFT:
                self._canvas.move(self._head, -self._grid_size, self._grid_size)
                self._facing = WEST
            elif direction == RIGHT:
                self._canvas.move(self._head, self._grid_size, self._grid_size)
                self._facing = EAST
            elif direction == BACKWARD:
                self._canvas.move(self._head, 0, self._grid_size * 2)
                self._facing = SOUTH
        elif facing == SOUTH:
            if direction == LEFT:
                self._canvas.move(self._head, self._grid_size, -self._grid_size)
                self._facing = EAST
            elif direction == RIGHT:
                self._canvas.move(self._head, -self._grid_size, -self._grid_size)
                self._facing = WEST
            elif direction == BACKWARD:
                self._canvas.move(self._head, 0, -self._grid_size * 2)
                self._facing = NORTH
        elif facing == EAST:
            if direction == LEFT:
                self._canvas.move(self._head, -self._grid_size, -self._grid_size)
                self._facing = NORTH
            elif direction == RIGHT:
                self._canvas.move(self._head, -self._grid_size, self._grid_size)
                self._facing = SOUTH
            elif direction == BACKWARD:
                self._canvas.move(self._head, -self._grid_size * 2, 0)
                self._facing = WEST
        else:
            if direction == LEFT:
                self._canvas.move(self._head, self._grid_size, self._grid_size)
                self._facing = SOUTH
            elif direction == RIGHT:
                self._canvas.move(self._head, self._grid_size, -self._grid_size)
                self._facing = NORTH
            elif direction == BACKWARD:
                self._canvas.move(self._head, self._grid_size * 2, 0)
                self._facing = EAST

        self.update()

    def move_robot(self, direction):
        switcher = {
            NORTH: self._north_facing_move,
            SOUTH: self._south_facing_move,
            EAST: self._east_facing_move,
            WEST: self._west_facing_move
        }

        f = switcher.get(self._facing)

        if direction == BACKWARD:
            self._turn_head(self._facing, RIGHT)
            self._turn_head(self._facing, RIGHT)
        elif direction != FORWARD:
            self._turn_head(self._facing, direction)

        f(direction)

    # def move_real_robot(self, sender, direction):
    #     self.turn_robot(sender, direction)
    #
    #     sender.send_arduino(get_arduino_cmd(FORWARD))
    #
    #     if self.facing == NORTH:
    #         self.center += 15
    #     elif self.facing == EAST:
    #         self.center += 1
    #     elif self.facing == SOUTH:
    #         self.center -= 15
    #     elif self.facing == WEST:
    #         self.center -= 1
    #
    #     updated_cells = self.mark_robot_standing()
    #
    #     sender.wait_arduino('D')
    #
    #     if ARROW_SCAN:
    #         self.check_arrow(sender)
    #
    #     return updated_cells

    def _north_facing_move(self, direction):
        switcher = {
            FORWARD: self._move_up,
            LEFT: self._move_left,
            RIGHT: self._move_right,
            BACKWARD: self._move_down
        }

        f = switcher.get(direction)

        f()

    def _south_facing_move(self, direction):
        switcher = {
            FORWARD: self._move_down,
            LEFT: self._move_right,
            RIGHT: self._move_left,
            BACKWARD: self._move_up
        }

        f = switcher.get(direction)

        f()

    def _east_facing_move(self, direction):
        switcher = {
            FORWARD: self._move_right,
            LEFT: self._move_up,
            RIGHT: self._move_down,
            BACKWARD: self._move_left
        }

        f = switcher.get(direction)

        f()

    def _west_facing_move(self, direction):
        switcher = {
            FORWARD: self._move_left,
            LEFT: self._move_down,
            RIGHT: self._move_up,
            BACKWARD: self._move_right
        }

        f = switcher.get(direction)

        f()

    def _move_up(self):
        self._canvas.move(self._robot_graphic, 0, -self._grid_size)
        self._canvas.move(self._head, 0, -self._grid_size)
        self.update()

    def _move_left(self):
        self._canvas.move(self._robot_graphic, -self._grid_size, 0)
        self._canvas.move(self._head, -self._grid_size, 0)
        self.update()

    def _move_right(self):
        self._canvas.move(self._robot_graphic, self._grid_size, 0)
        self._canvas.move(self._head, self._grid_size, 0)
        self.update()

    def _move_down(self):
        self._canvas.move(self._robot_graphic, 0, self._grid_size)
        self._canvas.move(self._head, 0, self._grid_size)
        self.update()

    # def _explore(self):
    #     # if not self._is_real_run:
    #     start_time = time()
    #     time_limit = float(self._time_limit_entry.get().strip())
    #     # if time_limit is negative, set to unlimited
    #     time_limit = time_limit if time_limit >= 0 else 10000000
    #     time_step = float(self._time_step_entry.get().strip())
    #
    #     # self._robot.real_map = self._grid_map
    #     exploration = Exploration(self._real_robot, start_time, float(self._explore_entry.get().strip()), time_limit)
    #     # run = exploration.start()
    #     run = exploration.start_real_efficient(self._sender)
    #     initial_pos = next(run)
    #     self.update_cells(initial_pos)
    #     while True:
    #         try:
    #             while True:
    #                 updated_cells = run.send(0)
    #                 self.update_cells(updated_cells)
    #
    #                 direction, move_or_turn, updated_cells = run.send(0)
    #                 sleep(time_step)
    #                 self._time_spent_label.config(text="%.2f" % get_time_elapsed(start_time) + "s")
    #                 self.update_cells(updated_cells)
    #
    #                 if move_or_turn == 0:
    #                     self.move_robot(direction)
    #                 elif move_or_turn == 1:
    #                     self._turn_head(self._facing, direction)
    #
    #                 is_complete = run.send(0)
    #                 if is_complete:
    #                     break
    #
    #                 is_looped = run.send(0)
    #                 if is_looped:
    #                     while True:
    #                         updated_or_moved, value, is_complete = run.send(0)
    #                         sleep(time_step)
    #                         self._time_spent_label.config(text="%.2f" % get_time_elapsed(start_time) + "s")
    #                         if updated_or_moved == "updated":
    #                             self.update_cells(value)
    #                         elif updated_or_moved == "moved":
    #                             self.move_robot(value)
    #                         else:
    #                             break
    #
    #                         if is_complete:
    #                             break
    #                     break
    #
    #             while True:
    #                 direction = run.send(0)
    #                 sleep(time_step)
    #                 self.move_robot(direction)
    #
    #         except StopIteration:
    #             print('EXPLORE_STR:', self._robot.get_explore_string())
    #             print('MAP_STR:', self._robot.get_map_string())
    #             break
    #     # else:
    #     #     self._explore_real()

    def _explore(self):
        start_time = time()
        exploration = Exploration(self._real_robot, start_time, 100.0, 720)

        run = exploration.start_real_efficient(self._sender)

        next(run)
        while True:
            try:
                # Exploration until completion

                while True:
                    updated_cells = run.send(0)
                    print('UPDATED', updated_cells)
                    self.update_cells(updated_cells)

                    direction, value, updated_cells = run.send(0)
                    self.update_cells(updated_cells)

                    if value == 0:
                        self.move_robot(direction)
                    elif value == 1:
                        self._turn_head(self._facing, direction)
                    is_complete = run.send(0)
                    if is_complete:
                        break

                    is_looped = run.send(0)
                    if is_looped:
                        while True:
                            updated_or_moved, value, is_complete = run.send(0)
                            if updated_or_moved == "updated" or updated_or_moved == "moved":
                                # self._update_android()
                                if updated_or_moved == "updated":
                                    self.update_cells(value)
                                elif updated_or_moved == "moved":
                                    self.move_robot(value)
                                    # updated_cells = self.move_robot(value)
                                    # self.update_cells(updated_cells)
                            else:
                                break

                            if is_complete:
                                break
                        break

                # Returning to start after completion
                while True:
                    direction = run.send(0)
                    self.move_robot(direction)

            except StopIteration:
                enable_print()
            print('EXPLORE_STR:', self._robot.get_explore_string())
            print('MAP_STR:', self._robot.get_map_string())
            disable_print()
            print('Returned to start!')
            if self._robot.facing == WEST:
                print('ENTERED FACING WEST')
                self._robot.turn_robot(self._sender, LEFT)
                # self._calibrate()
            elif self._robot.facing == SOUTH:
                print('ENTERED FACING SOUTH')
                self._sender.send_arduino('c')
                # self._calibrate()
            break

    def _explore_real(self):
        start_time = time()
        time_limit = float(self._time_limit_entry.get().strip())
        # if time_limit is negative, set to unlimited
        time_limit = time_limit if time_limit >= 0 else 10000000
        time_step = float(self._time_step_entry.get().strip())
        self._robot.real_map = self._grid_map
        exploration = Exploration(self._robot, start_time, float(self._explore_entry.get().strip()), time_limit)
        run = exploration.start()
        initial_pos = next(run)
        self.update_cells(initial_pos)
        while True:
            try:
                while True:
                    updated_cells = run.send(0)
                    self.update_cells(updated_cells)

                    direction, move_or_turn, updated_cells = run.send(0)
                    sleep(time_step)
                    self._time_spent_label.config(text="%.2f" % get_time_elapsed(start_time) + "s")
                    self.update_cells(updated_cells)

                    if move_or_turn == 0:
                        self.move_robot(direction)
                    elif move_or_turn == 1:
                        self._turn_head(self._facing, direction)

                    is_complete = run.send(0)
                    if is_complete:
                        break

                    is_looped = run.send(0)
                    if is_looped:
                        while True:
                            updated_or_moved, value, is_complete = run.send(0)
                            sleep(time_step)
                            self._time_spent_label.config(text="%.2f" % get_time_elapsed(start_time) + "s")
                            if updated_or_moved == "updated":
                                self.update_cells(value)
                            elif updated_or_moved == "moved":
                                self.move_robot(value)
                            else:
                                break

                            if is_complete:
                                break
                        break

                while True:
                    direction = run.send(0)
                    sleep(time_step)
                    self.move_robot(direction)

            except StopIteration:
                print('EXPLORE_STR:', self._robot.get_explore_string())
                print('MAP_STR:', self._robot.get_map_string())
                break

    def update_cells(self, updated_cells):
        start_cells = get_robot_cells(17)
        goal_cells = get_robot_cells(284)
        for cell, value in updated_cells.items():
            if cell in start_cells:
                self.mark_cell(cell, "#30807D")
            elif cell in goal_cells:
                self.mark_cell(cell, "#08AE69")
            elif not value:
                self.mark_cell(cell, "#F3F3F3")
            else:
                self.mark_cell(cell, "#F44336")

        self._percentage_completion_label.config(text=("%.2f" % self._robot.get_completion_percentage() + "%"))

    def _load_map(self):
        filename = askopenfilename(title="Select Map Descriptor", filetypes=[("Text Files (*.txt)", "*.txt")])

        if filename:
            print(filename)
            if self._parse_map(filename):
                self._paint_map()
                return True
            print("File %s cannot be parsed" % filename)
            return False
        print("File %s does not exist" % filename)
        return False

    def _move_fastest_path(self, fastest_path):
        time_step = float(self._time_step_entry.get().strip())
        if fastest_path:
            for move in fastest_path:
                sleep(time_step)
                self._robot.move_robot(move)
                self.move_robot(move)
        else:
            print("No valid path")

    def _find_fastest_path(self):
        for row in range(20):
            for col in range(15):
                try:
                    if self._grid_map[row][col] == 3:
                        self._mark_open(row * 15 + col + 1)
                except AttributeError:
                    continue

        fastest_path_start_way_point = fp.get_shortest_path_moves(self._robot,
                                                                  start=(1, 1),
                                                                  goal=self.way_point)
        self._move_fastest_path(fastest_path_start_way_point)

        before_way_point = previous_cell(self._robot.center, self._robot.facing)
        fastest_path_way_point_goal = fp.get_shortest_path_moves(self._robot,
                                                                 start=self.way_point,
                                                                 goal=(18, 13),
                                                                 before_start_point=before_way_point)
        self._move_fastest_path(fastest_path_way_point_goal)

    def _mark_wall(self, grid_num):
        self._canvas.itemconfig(grid_num, fill="#f44336")
        self.update()

    def _mark_open(self, grid_num):
        self._canvas.itemconfig(grid_num, fill="#f3f3f3")
        self.update()

    def _mark_path(self, grid_num):
        self._canvas.itemconfig(grid_num, fill="#43bc98")
        self.update()

    def _mark_way_point(self, grid_num):
        self._canvas.itemconfig(grid_num, fill="#ffc700")
        self.update()

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

    def _paint_map(self):
        for i in range(20):
            for j in range(15):
                grid_num = i * 15 + j + 1
                self.mark_cell(grid_num, "#1A1E24")

    def mark_cell(self, cell_index, cell_type):
        self._canvas.itemconfig(cell_index, fill=cell_type)
        self.update()

    def _on_grid_click(self, event, arg):
        try:
            self._mark_open(self.way_point[0] * 15 + self.way_point[1] + 1)
        except AttributeError:
            pass

        self.way_point = (19 - int(event.y/30), int(event.x/30))
        self._mark_way_point(self.way_point[0] * 15 + self.way_point[1] + 1)
        event.widget.itemconfig(arg, activefill="#00ffff")


def get_time_elapsed(start_time):
    return float(time() - start_time)
