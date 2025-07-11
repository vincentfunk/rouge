import random

from locations.map import Map
from locations.grid import Grid
from entities.player import Player
from entities.monster import Monster
class Game:
    def __init__(self, ysize, xsize):
        self.map = Map(ysize, xsize)
        self.actorGrid = Grid(ysize, xsize)
        self.player = None
        self.addPlayer()
        self.monsters = []
        self.addMonsters()

    def round(self, input):
        """one game round starting with player action then monster actions"""
        if input in "wsad":
            self.player.move(input)

        for mon in self.monsters:
            # move closer logic to monster class and improve sidestep thing
            # closer = self.closerDirect(mon, self.player)
            mon.moveCloser()

    def addPlayer(self):
        """creates player"""
        y, x = self.map.randInsidePoint()
        self.player = Player(self, y, x)

    def addMonsters(self):
        """adds monsters"""
        for i in range(3):
            y, x = self.map.randInsidePoint()
            self.monsters.append(Monster(self, y, x))

    def board(self):
        """outputs string of actorGrid overlaid over map.grid"""
        out = '+' + '-' * len(self.map.grid[0]) + '+' + '\n'
        for y in range(len(self.map.grid)):
            out += '|'
            for x in range(len(self.map.grid[0])):
                if self.actorGrid[y][x] != ' ':
                    out += self.actorGrid[y][x]
                else:
                    out += self.map.grid[y][x]
            out += '|\n'
        out += '+' + '-' * len(self.map.grid[0]) + '+'
        return out

    # def comparePos(self, e1, e2):
    #     """1  3
    #         e2
    #        6  8"""
    #     if e1.y <= e2.y and e1.x <= e2.x:
    #         return 1
    #     elif e1.y <= e2.y and e1.x > e2.x:
    #         return 3
    #     elif e1.y > e2.y and e1.x <= e2.x:
    #         return 6
    #     else:
    #         return 8
    #
    # def closerDirect(self, e1, e2):
    #     sector = self.comparePos(e1, e2)
    #     if sector == 1:
    #         return "s" if random.randint(0, 1) else "d"
    #     elif sector == 3:
    #         return "s" if random.randint(0, 1) else "a"
    #     elif sector == 6:
    #         return "w" if random.randint(0, 1) else "d"
    #     elif sector == 8:
    #         return "w" if random.randint(0, 1) else "a"