from locations.grid import Grid
from locations.room import Room
from locations.hall import Hall
import random


class Map:
    def __init__(self, ysize, xsize):
        self.ysize = ysize
        self.xsize = xsize
        self.grid = Grid(ysize, xsize)
        self.rooms = None
        self.halls = None
        self.create()
        self.next = self.next()

    def valid_moves(self):
        """create list of valid inside points"""
        moves = []
        for room in self.rooms:
            for point in room.allInsidePoints():
                moves.append(point)
        for hall in self.halls:
            for point in hall.all_points():
                moves.append(point)
        return moves

    def rand_inside_point(self):
        """pick a random point inside a random room"""
        room = random.randint(0, len(self.rooms) - 1)
        y = random.randint(self.rooms[room].ymin + 1, self.rooms[room].ymax - 1)
        x = random.randint(self.rooms[room].xmin + 1, self.rooms[room].xmax - 1)
        return y, x

    def create(self):
        """creates the map"""
        room_count = random.randint(5, 7)
        hall_count = random.randint(room_count - 1, room_count + 1)
        for i in range(room_count + 1):
            self.add_room()
        for i in range(hall_count + 1):
            self.add_hall()
        # multiple connections and disconnected checks
        while self.rooms_disconnected():
            try:
                self.add_hall(self.rooms_disconnected()[0])
            except RecursionError:
                self.add_hall(self.rooms_disconnected()[1])

    def rooms_disconnected(self):
        """returns list of rooms disconnected from the first room"""
        begin = 0
        while True:
            connected = [self.rooms[begin]]
            for room in connected:
                for hall in self.halls:
                    if hall.room1 is room and hall.room2 not in connected:
                        connected.append(hall.room2)
                    elif hall.room2 is room and hall.room1 not in connected:
                        connected.append(hall.room1)
            disconnected = [room for room in self.rooms if room not in connected]
            if len(disconnected) < len(self.rooms) / 2 + 1:
                return disconnected
            begin += 1
        # return disconnected

    def add_room(self):
        """adds a new random non-overlapped room"""
        while True:
            new = self.rand_room()
            if not self.too_close(new):
                break
        if self.rooms is None:
            self.rooms = [new]
        else:
            self.rooms.append(new)
        self.grid.draw_room(new) # , len(self.rooms)) # this is room marker

    def rand_room(self):
        """returns a random room"""
        ystart = random.randint(0, self.ysize - 4)
        xstart = random.randint(0, self.xsize - 4)
        yspace = self.ysize - ystart - 2
        xspace = self.xsize - xstart - 2
        # if not enough space reroll the room
        if yspace < 3 or xspace < 3:
            return self.rand_room()
        # internal length
        ylen = random.randint(3, min(10, yspace))
        xlen = random.randint(3, min(20, xspace))
        return Room(ystart, xstart, ystart + ylen + 1, xstart + xlen + 1)

    def too_close(self, room):
        """checks a room against all current rooms to find overlaps"""
        if self.rooms is None:
            return False
        for cord in room.all_points():
            for existing in self.rooms:
                if existing.is_close(cord):
                    return True
        return False

    def is_overlap(self, hall):
        """checks a hall against all current rooms to find overlaps"""
        for cord in hall.all_points()[1:-1]:
            for existing in self.rooms:
                if existing.is_inside(cord):
                    return True
        return False

    def add_hall(self, force=None):
        """adds a new hall to the map"""
        count = 0
        max_attempts = 100
        while True:
            # stops a hall that cant connect from looping forever
            count += 1
            if count > max_attempts:
                raise RecursionError("too many attempts")

            new = self.rand_hall(force)
            # rerolls immediately if corner is same as start
            # this is a bug fix might be a better way by fixing hall definition itself
            while new.start == new.corner:
                new = self.rand_hall(force)
            # check that hall does not overlap a room or connect two previously connected rooms

            if not self.is_overlap(new) and not self.connected(new.room1, new.room2):
                break
        if self.halls is None:
            self.halls = [new]
        else:
            self.halls.append(new)
        self.grid.draw_hall(new)

    def connected(self, r1, r2):
        """checks if two rooms are connected by a hall"""
        if self.halls is None:
            return False
        for hall in self.halls:
            if hall.room1 == r1 and hall.room2 == r2:
                return True
        return False

    def rand_hall(self, force=None):
        """generates a random hall between two rooms"""
        # pick 2 rooms
        if force:
            while True:
                r1 = force
                r2 = random.choice(self.rooms)
                if r1 != r2: # and not self.connected(r1, r2):
                    break
        else:
            while True:
                r1 = random.choice(self.rooms)
                r2 = random.choice(self.rooms)
                if r1 != r2: # and not self.connected(r1, r2):
                    break

        sec = self.calc_sector(r1, r2)
        # flip rooms
        if sec in [5, 6, 7, 8]:
            r1, r2 = r2, r1
        # horizontal hall
        if sec in [4, 5]:
            if r1.ymin >= r2.ymin and r1.ymax <= r2.ymax:  # r1 inside r2
                y = random.randint(r1.ymin + 1, r1.ymax - 1)
            elif r1.ymin <= r2.ymin and r1.ymax >= r2.ymax:  # r2 inside r1
                y = random.randint(r2.ymin + 1, r2.ymax - 1)
            elif r1.ymin >= r2.ymin:  # r1 below r2
                y = random.randint(r1.ymin + 1, r2.ymax - 1)
            elif r1.ymax <= r2.ymax:  # r1 above r2
                y = random.randint(r2.ymin + 1, r1.ymax - 1)
            return Hall(r1, r2, (y, r1.xmax), (y, r2.xmin))
        # vertical hall
        elif sec in [2, 7]:
            if r1.xmin >= r2.xmin and r1.xmax <= r2.xmax:  # r1 inside r2
                x = random.randint(r1.xmin + 1, r1.xmax - 1)
            elif r1.xmin <= r2.xmin and r1.xmax >= r2.xmax:  # r2 inside r1
                x = random.randint(r2.xmin + 1, r2.xmax - 1)
            elif r1.xmin >= r2.xmin:  # r1 right of r2
                x = random.randint(r1.xmin + 1, r2.xmax - 1)
            elif r1.xmax <= r2.xmax:  # r1 left of r2
                x = random.randint(r2.xmin + 1, r1.xmax - 1)
            return Hall(r1, r2, (r1.ymax, x), (r2.ymin, x))
        # above and left/below and right
        elif sec in [1, 8, 3, 6]:
            # select between two possible side choices
            rand = random.randint(0, 1)
            if rand:
                r1y = r1.ymax
                r1x = random.randint(r1.xmin + 1, r1.xmax - 1)
                r2y = random.randint(r2.ymin + 1, r2.ymax - 1)
                if sec in [1, 8]:
                    r2x = r2.xmin
                elif sec in [3, 6]:
                    r2x = r2.xmax
                cor = (r2y, r1x)
            else:
                r1y = random.randint(r1.ymin + 1, r1.ymax - 1)
                if sec in [1, 8]:
                    r1x = r1.xmax
                elif sec in [3, 6]:
                    r1x = r1.xmin
                r2y = r2.ymin
                r2x = random.randint(r2.xmin + 1, r2.xmax - 1)
                cor = (r1y, r2x)
            return Hall(r1, r2, (r1y, r1x), (r2y, r2x), cor)

    def calc_sector(self, r1, r2):
        """compare two rooms locations with room2 as the center
        123
        4 5
        678
        """
        if r1.ymax - 1 <= r2.ymin and r1.xmax - 1 <= r2.xmin:
            sec = 1
        elif r1.ymax - 1 <= r2.ymin and r1.xmin >= r2.xmax - 1:
            sec = 3
        elif r1.ymin >= r2.ymax - 1 and r1.xmax - 1 <= r2.xmin:
            sec = 6
        elif r1.ymin >= r2.ymax - 1 and r1.xmin >= r2.xmax - 1:
            sec = 8
        elif r1.ymax <= r2.ymin:
            sec = 2
        elif r1.ymin >= r2.ymax:
            sec = 7
        elif r1.xmax <= r2.xmin:
            sec = 4
        elif r1.xmin >= r2.xmax:
            sec = 5
        else:
            raise ValueError("Sector calculation failed")
        return sec

    def next(self):
        point = self.rand_inside_point()
        self.grid[point[0]][point[1]] = '>'
        return point
