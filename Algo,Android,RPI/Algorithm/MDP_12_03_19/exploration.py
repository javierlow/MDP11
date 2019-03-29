from fastest_path import *


class ExploreComplete(Exception):
    def __init__(self, message="Exploration complete!"):
        print(message)


class CellsUpdated(Exception):
    pass


class PathNotFound(Exception):
    def __init__(self):
        print("Valid path not found!")


class Exploration:
    def __init__(self, robot, start_time, exploration_limit=100, time_limit=360):
        self._robot = robot
        self._start_time = start_time
        self._exploration_limit = exploration_limit
        self._time_limit = time_limit
        self._auto_update = True

    def _get_nearest_unexplored(self):
        min_dist = 301
        nearest = (-1, -1)
        for i in range(20):
            for j in range(15):
                if self._robot.discovered_map[i][j] == 2:
                    y, x = get_coordinates(self._robot.center)
                    dist = abs(y - i) + abs(x - j)

                    if dist < min_dist:
                        min_dist = dist
                        nearest = (i, j)

        return nearest[0], nearest[1]

    def start_real_simulation(self, sender):
        yield self._robot.mark_robot_standing()

        is_back_at_start = False
        while True:
            try:
                while not is_back_at_start:
                    updated_cells = self._robot.get_sensor_readings(sender)
                    yield updated_cells

                    if self._robot.check_free(LEFT) and not self._robot.in_efficiency_limit():
                        updated_cells = self._robot.move_robot(sender, LEFT)
                        yield LEFT, 0, updated_cells
                    elif self._robot.check_free(FORWARD):
                        updated_cells = self._robot.move_robot(sender, FORWARD)
                        yield FORWARD, 0, updated_cells
                    else:
                        if self._robot.in_efficiency_limit():
                            if self._robot.check_free(LEFT):
                                updated_cells = self._robot.move_robot(sender, LEFT)
                                yield LEFT, 0, updated_cells
                                yield self._robot.is_complete(self._exploration_limit, self._start_time,
                                                              self._time_limit)
                                if self._robot.is_complete(self._exploration_limit, self._start_time,
                                                           self._time_limit):
                                    raise ExploreComplete

                                if self._robot.center == 17:
                                    is_back_at_start = True
                                yield is_back_at_start
                                if is_back_at_start:
                                    break
                                updated_cells = self._robot.get_sensor_readings(sender)
                                yield updated_cells
                                self._robot.turn_robot(sender, RIGHT)
                                self._robot.turn_robot(sender, RIGHT)
                                yield BACKWARD, 1, {}
                        else:
                            self._robot.turn_robot(sender, RIGHT)
                            yield RIGHT, 1, {}

                    is_complete = self._robot.is_complete(self._exploration_limit, self._start_time, self._time_limit)
                    yield is_complete
                    if is_complete:
                        raise ExploreComplete

                    if self._robot.center == 17:
                        is_back_at_start = True
                        print("looped")

                    yield is_back_at_start

                if self._robot.get_completion_percentage() >= 100:
                    return True

                while True:
                    try:
                        nearest_unexplored_y, nearest_unexplored_x = self._get_nearest_unexplored()
                        center_y, center_x = get_coordinates(self._robot.center)

                        moves = get_shortest_path_moves(self._robot,
                                                        (center_y, center_x),
                                                        (nearest_unexplored_y, nearest_unexplored_x))

                        if not moves:  # Check adjacent cells
                            adjacent_cells = get_robot_cells(get_grid_index(nearest_unexplored_y, nearest_unexplored_x))
                            del adjacent_cells[4]

                            adj_order = [5, 6, 7, 3, 4, 0, 1, 2]
                            adjacent_cells = [adjacent_cells[i] for i in adj_order]

                            moves = get_shortest_valid_path(self._robot,
                                                            self._robot.center, adjacent_cells)

                            if not moves:
                                corner_cells = [adjacent_cells[0], adjacent_cells[2], adjacent_cells[5],
                                                adjacent_cells[7]]

                                for cell in corner_cells:
                                    double_adjacent_cells = get_robot_cells(cell)
                                    if corner_cells.index(cell) == 0:
                                        unwanted = set(double_adjacent_cells[1:3])
                                        unwanted.update(double_adjacent_cells[4:6])
                                    elif corner_cells.index(cell) == 1:
                                        unwanted = set(double_adjacent_cells[0:2])
                                        unwanted.update(double_adjacent_cells[3:5])
                                    elif corner_cells.index(cell) == 2:
                                        unwanted = set(double_adjacent_cells[4:6])
                                        unwanted.update(double_adjacent_cells[7:9])
                                    elif corner_cells.index(cell) == 3:
                                        unwanted = set(double_adjacent_cells[3:5])
                                        unwanted.update(double_adjacent_cells[6:8])

                                    double_adjacent_cells = [e for e in double_adjacent_cells if e not in unwanted]

                                    moves = get_shortest_valid_path(self._robot,
                                                                    self._robot.center, double_adjacent_cells)
                                    if moves:
                                        break

                        if not moves:
                            raise PathNotFound

                        updated_cells = self._robot.get_sensor_readings(sender)
                        for move in moves:
                            if updated_cells:
                                is_complete = self._robot.is_complete(self._exploration_limit, self._start_time,
                                                                      self._time_limit)
                                yield "updated", updated_cells, is_complete
                                if is_complete:
                                    raise ExploreComplete
                                raise CellsUpdated
                            updated_cells = self._robot.move_robot(sender, move)
                            yield "moved", move, False

                    except CellsUpdated:
                        continue

            except ExploreComplete:
                break
            except PathNotFound:
                yield "invalid", None, None
                break

        print("Returning to Start...")

        while True:
            center_y, center_x = get_coordinates(self._robot.center)
            start_y, start_x = get_coordinates(17)

            try:
                moves = get_shortest_path_moves(self._robot,
                                                (center_y, center_x), (start_y, start_x), is_give_up=True)

                if not moves:
                    break

                for move in moves:
                    updated_cells = self._robot.get_sensor_readings(sender)
                    if updated_cells:
                        yield move
                        raise CellsUpdated
                    self._robot.move_robot(sender, move)
                    yield move

            except IndexError:
                break
            except CellsUpdated:
                continue

        return True

    def start(self):
        yield self._robot.mark_robot_standing()

        is_back_at_start = False
        while True:
            try:
                while not is_back_at_start:
                    updated_cells = self._robot.get_sensor_readings()
                    yield updated_cells

                    if self._robot.check_free(LEFT) and not \
                            self._robot.in_efficiency_limit():
                        updated_cells = self._robot.move_robot(LEFT)
                        yield LEFT, 0, updated_cells
                    elif self._robot.check_free(FORWARD):
                        updated_cells = self._robot.move_robot(FORWARD)
                        yield FORWARD, 0, updated_cells
                    else:
                        if self._robot.in_efficiency_limit():
                            if self._robot.check_free(LEFT):
                                updated_cells = self._robot.move_robot(LEFT)
                                yield LEFT, 0, updated_cells
                                yield self._robot.is_complete(self._exploration_limit, self._start_time,
                                                              self._time_limit)
                                if self._robot.is_complete(self._exploration_limit, self._start_time,
                                                           self._time_limit):
                                    raise ExploreComplete

                                if self._robot.center == 17:
                                    is_back_at_start = True
                                yield is_back_at_start
                                if is_back_at_start:
                                    break
                                updated_cells = self._robot.get_sensor_readings()
                                yield updated_cells
                                self._robot.turn_robot(BACKWARD)
                                yield BACKWARD, 1, {}
                        else:
                            self._robot.turn_robot(RIGHT)
                            yield RIGHT, 1, {}

                    yield self._robot.is_complete(self._exploration_limit, self._start_time, self._time_limit)
                    if self._robot.is_complete(self._exploration_limit, self._start_time, self._time_limit):
                        raise ExploreComplete

                    if self._robot.center == 17:
                        is_back_at_start = True

                    yield is_back_at_start

                while True:
                    try:
                        nearest_unexplored_y, nearest_unexplored_x = self._get_nearest_unexplored()
                        center_y, center_x = get_coordinates(self._robot.center)

                        moves = get_shortest_path_moves(self._robot,
                                                        (center_y, center_x),
                                                        (nearest_unexplored_y, nearest_unexplored_x))

                        if not moves:
                            adjacent_cells = get_robot_cells(get_grid_index(nearest_unexplored_y, nearest_unexplored_x))
                            del adjacent_cells[4]

                            adj_order = [5, 6, 7, 3, 4, 0, 1, 2]
                            adjacent_cells = [adjacent_cells[i] for i in adj_order]

                            moves = get_shortest_valid_path(self._robot,
                                                            self._robot.center, adjacent_cells)

                            if not moves:
                                corner_cells = [adjacent_cells[0], adjacent_cells[2], adjacent_cells[5],
                                                adjacent_cells[7]]

                                for cell in corner_cells:
                                    double_adjacent_cells = get_robot_cells(cell)
                                    if corner_cells.index(cell) == 0:
                                        unwanted = set(double_adjacent_cells[1:3])
                                        unwanted.update(double_adjacent_cells[4:6])
                                    elif corner_cells.index(cell) == 1:
                                        unwanted = set(double_adjacent_cells[0:2])
                                        unwanted.update(double_adjacent_cells[3:5])
                                    elif corner_cells.index(cell) == 2:
                                        unwanted = set(double_adjacent_cells[4:6])
                                        unwanted.update(double_adjacent_cells[7:9])
                                    elif corner_cells.index(cell) == 3:
                                        unwanted = set(double_adjacent_cells[3:5])
                                        unwanted.update(double_adjacent_cells[6:8])

                                    double_adjacent_cells = [e for e in double_adjacent_cells if e not in unwanted]

                                    moves = get_shortest_valid_path(self._robot,
                                                                    self._robot.center, double_adjacent_cells)
                                    if moves:
                                        break

                        if not moves:
                            raise PathNotFound

                        for move in moves:
                            updated_cells = self._robot.get_sensor_readings()
                            if updated_cells:
                                yield "updated", updated_cells, \
                                      self._robot.is_complete(self._exploration_limit, self._start_time,
                                                              self._time_limit)
                                if self._robot.is_complete(self._exploration_limit, self._start_time,
                                                           self._time_limit):
                                    raise ExploreComplete
                                raise CellsUpdated
                            self._robot.move_robot(move)
                            yield "moved", move, False

                    except CellsUpdated:
                        continue

            except ExploreComplete:
                break
            except PathNotFound:
                yield "invalid", None, None
                break

        print("Returning to Start...")

        center_y, center_x = get_coordinates(self._robot.center)
        start_y, start_x = get_coordinates(17)

        moves = get_shortest_path_moves(self._robot,
                                        (center_y, center_x), (start_y, start_x), is_give_up=True)

        for move in moves:
            self._robot.move_robot(move)
            yield move

        return True

    def start_real(self, sender):
        yield self._robot.mark_robot_standing()

        is_back_at_start = False
        while True:
            try:
                while not is_back_at_start:
                    updated_cells = self._robot.get_sensor_readings(sender)
                    yield updated_cells

                    if self._robot.check_free(LEFT):
                        updated_cells = self._robot.move_robot(sender, LEFT)
                        yield LEFT, 0, updated_cells
                    elif self._robot.check_free(FORWARD):
                        updated_cells = self._robot.move_robot(sender, FORWARD)
                        yield FORWARD, 0, updated_cells
                    elif self._robot.check_free(RIGHT):
                        updated_cells = self._robot.move_robot(sender, RIGHT)
                        yield RIGHT, 0, updated_cells
                    else:
                        self._robot.turn_robot(sender, BACKWARD)
                        yield BACKWARD, 1, {}

                    is_complete = self._robot.is_complete(self._exploration_limit, self._start_time, self._time_limit)
                    yield is_complete
                    if is_complete:
                        raise ExploreComplete

                    if self._robot.center == 17:
                        is_back_at_start = True
                        print("looped")

                    yield is_back_at_start

                if self._robot.get_completion_percentage() >= 100:
                    return True

                while True:
                    try:
                        nearest_unexplored_y, nearest_unexplored_x = self._get_nearest_unexplored()
                        center_y, center_x = get_coordinates(self._robot.center)

                        moves = get_shortest_path_moves(self._robot,
                                                        (center_y, center_x),
                                                        (nearest_unexplored_y, nearest_unexplored_x))

                        if not moves:
                            adjacent_cells = get_robot_cells(get_grid_index(nearest_unexplored_y, nearest_unexplored_x))
                            del adjacent_cells[4]

                            adj_order = [5, 6, 7, 3, 4, 0, 1, 2]
                            adjacent_cells = [adjacent_cells[i] for i in adj_order]

                            moves = get_shortest_valid_path(self._robot,
                                                            self._robot.center, adjacent_cells)

                            if not moves:
                                corner_cells = [adjacent_cells[0], adjacent_cells[2], adjacent_cells[5],
                                                adjacent_cells[7]]

                                for cell in corner_cells:
                                    double_adjacent_cells = get_robot_cells(cell)
                                    if corner_cells.index(cell) == 0:
                                        unwanted = set(double_adjacent_cells[1:3])
                                        unwanted.update(double_adjacent_cells[4:6])
                                    elif corner_cells.index(cell) == 1:
                                        unwanted = set(double_adjacent_cells[0:2])
                                        unwanted.update(double_adjacent_cells[3:5])
                                    elif corner_cells.index(cell) == 2:
                                        unwanted = set(double_adjacent_cells[4:6])
                                        unwanted.update(double_adjacent_cells[7:9])
                                    elif corner_cells.index(cell) == 3:
                                        unwanted = set(double_adjacent_cells[3:5])
                                        unwanted.update(double_adjacent_cells[6:8])

                                    double_adjacent_cells = [e for e in double_adjacent_cells if e not in unwanted]

                                    moves = get_shortest_valid_path(self._robot,
                                                                    self._robot.center, double_adjacent_cells)
                                    if moves:
                                        break

                        if not moves:
                            raise PathNotFound

                        updated_cells = self._robot.get_sensor_readings(sender)
                        for move in moves:
                            if updated_cells:
                                is_complete = self._robot.is_complete(self._exploration_limit, self._start_time,
                                                                      self._time_limit)
                                yield "updated", updated_cells, is_complete
                                if is_complete:
                                    raise ExploreComplete
                                raise CellsUpdated
                            updated_cells = self._robot.move_robot(sender, move)
                            yield "moved", move, False

                    except CellsUpdated:
                        continue

            except ExploreComplete:
                break
            except PathNotFound:
                yield "invalid", None, None
                break

        # Return to start after completion

        print("Returning to Start...")

        while True:
            center_y, center_x = get_coordinates(self._robot.center)
            start_y, start_x = get_coordinates(17)

            try:
                moves = get_shortest_path_moves(self._robot,
                                                (center_y, center_x), (start_y, start_x), is_give_up=True)

                if not moves:
                    break

                for move in moves:
                    updated_cells = self._robot.get_sensor_readings(sender)
                    if updated_cells:
                        yield move
                        raise CellsUpdated
                    self._robot.move_robot(sender, move)
                    yield move

            except IndexError:
                break
            except CellsUpdated:
                continue

        return True

    def start_real_efficient(self, sender):
        yield self._robot.mark_robot_standing()

        is_back_at_start = False
        while True:
            try:
                while not is_back_at_start:
                    updated_cells = self._robot.get_sensor_readings(sender)
                    yield updated_cells

                    if self._robot.check_free(LEFT) and not self._robot.in_efficiency_limit():
                        updated_cells = self._robot.move_robot(sender, LEFT)
                        yield LEFT, 0, updated_cells
                    elif self._robot.check_free(FORWARD):
                        updated_cells = self._robot.move_robot(sender, FORWARD)
                        yield FORWARD, 0, updated_cells
                    else:
                        if self._robot.in_efficiency_limit():
                            if self._robot.check_free(LEFT):
                                updated_cells = self._robot.move_robot(sender, LEFT)
                                yield LEFT, 0, updated_cells
                                yield self._robot.is_complete(self._exploration_limit, self._start_time,
                                                              self._time_limit)
                                if self._robot.is_complete(self._exploration_limit, self._start_time,
                                                           self._time_limit):
                                    raise ExploreComplete

                                if self._robot.center == 17:
                                    is_back_at_start = True
                                yield is_back_at_start
                                if is_back_at_start:
                                    break
                                updated_cells = self._robot.get_sensor_readings(sender)
                                yield updated_cells
                                self._robot.turn_robot(sender, BACKWARD)
                                yield BACKWARD, 1, {}
                        else:
                            self._robot.turn_robot(sender, RIGHT)
                            yield RIGHT, 1, {}

                    is_complete = self._robot.is_complete(self._exploration_limit, self._start_time, self._time_limit)
                    yield is_complete
                    if is_complete:
                        raise ExploreComplete

                    if self._robot.center == 17:
                        is_back_at_start = True
                        print("looped")

                    yield is_back_at_start

                if self._robot.get_completion_percentage() == 100:
                    return True

                while True:
                    try:
                        nearest_unexplored_y, nearest_unexplored_x = self._get_nearest_unexplored()
                        center_y, center_x = get_coordinates(self._robot.center)

                        moves = get_shortest_path_moves(self._robot,
                                                        (center_y, center_x),
                                                        (nearest_unexplored_y, nearest_unexplored_x))

                        if not moves:  # Check adjacent cells
                            adjacent_cells = get_robot_cells(get_grid_index(nearest_unexplored_y, nearest_unexplored_x))
                            del adjacent_cells[4]

                            adj_order = [5, 6, 7, 3, 4, 0, 1, 2]
                            adjacent_cells = [adjacent_cells[i] for i in adj_order]

                            moves = get_shortest_valid_path(self._robot,
                                                            self._robot.center, adjacent_cells)

                            if not moves:
                                corner_cells = [adjacent_cells[0], adjacent_cells[2], adjacent_cells[5],
                                                adjacent_cells[7]]

                                for cell in corner_cells:
                                    double_adjacent_cells = get_robot_cells(cell)
                                    if corner_cells.index(cell) == 0:
                                        unwanted = set(double_adjacent_cells[1:3])
                                        unwanted.update(double_adjacent_cells[4:6])
                                    elif corner_cells.index(cell) == 1:
                                        unwanted = set(double_adjacent_cells[0:2])
                                        unwanted.update(double_adjacent_cells[3:5])
                                    elif corner_cells.index(cell) == 2:
                                        unwanted = set(double_adjacent_cells[4:6])
                                        unwanted.update(double_adjacent_cells[7:9])
                                    elif corner_cells.index(cell) == 3:
                                        unwanted = set(double_adjacent_cells[3:5])
                                        unwanted.update(double_adjacent_cells[6:8])

                                    double_adjacent_cells = [e for e in double_adjacent_cells if e not in unwanted]

                                    moves = get_shortest_valid_path(self._robot,
                                                                    self._robot.center, double_adjacent_cells)
                                    if moves:
                                        break

                        if not moves:
                            raise PathNotFound

                        updated_cells = self._robot.get_sensor_readings(sender)
                        for move in moves:
                            if updated_cells:
                                is_complete = self._robot.is_complete(self._exploration_limit, self._start_time,
                                                                      self._time_limit)
                                yield "updated", updated_cells, is_complete
                                if is_complete:
                                    raise ExploreComplete
                                raise CellsUpdated
                            updated_cells = self._robot.move_robot(sender, move)
                            yield "moved", move, False

                    except CellsUpdated:
                        continue

            except ExploreComplete:
                break
            except PathNotFound:
                yield "invalid", None, None
                break

        print("Returning to Start...")

        while True:
            center_y, center_x = get_coordinates(self._robot.center)
            start_y, start_x = get_coordinates(17)

            try:
                moves = get_shortest_path_moves(self._robot,
                                                (center_y, center_x), (start_y, start_x), is_give_up=True)

                if not moves:
                    break

                for move in moves:
                    updated_cells = self._robot.get_sensor_readings(sender)
                    if updated_cells:
                        yield move
                        raise CellsUpdated
                    self._robot.move_robot(sender, move)
                    yield move

            except IndexError:
                break
            except CellsUpdated:
                continue

        return True
