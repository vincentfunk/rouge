import math
import random

from locations.room import Room

class Grid(list):
    def __init__(self, y=None, x=None, grid=None):
        super().__init__()
        self.adjacent = []
        if grid is None:
            for line in range(y):
                self.append([' '] * x)
        else:
            for line in grid:
                self.append([pos for pos in line])

    def display(self):
        """print self with borders"""
        print('+' + '-' * len(self[0]) + '+')
        for line in self:
            print('|', end="")
            for pos in line:
                print(pos, end="")
            print('|')
        print('+' + '-' * len(self[0]) + '+')

    def str(self):
        """string representation of grid"""
        out = '+' + '-' * len(self[0]) + '+' + '\n'
        for line in self:
            out += '|'
            for pos in line:
                out+= pos
            out += '|\n'
        out += '+' + '-' * len(self[0]) + '+'
        return out

    def draw_room(self, room, mark='+'):
        """writes room onto grid(self)"""
        if not isinstance(room, Room):
            raise ValueError("Not a room")
        for y, x in room.cords:
            self[y][x] = mark
        inside_len = room.xmax - room.xmin - 1
        for y in range(room.ymin + 1, room.ymax):
            self[y][room.xmin:room.xmax + 1] = '|' + '·' * inside_len + '|'
        self[room.ymin][room.xmin + 1:room.xmax] = '-' * inside_len
        self[room.ymax][room.xmin + 1:room.xmax] = '-' * inside_len

    def draw_hall(self, hall):
        """draws a hall on the map with the first and last points being the doors"""
        points = list(hall.all_points())
        y, x = points[0]
        self[y][x] = '+'
        for y, x in points[1:]:
            self[y][x] = '#'
        else:
            self[y][x] = '+'

    def rand_point(self, symbol):
        """find random point of certain symbol"""
        while True:
            x = random.randint(0, len(self[0]) - 1)
            y = random.randint(0, len(self) - 1)
            if self[y][x] == symbol:
                return y, x

