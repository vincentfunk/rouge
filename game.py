import random

from locations.map import Map
from locations.grid import Grid
from entities.player import Player
from entities.monster import Monster


class Game:
    def __init__(self, ysize, xsize, player=None):
        self.map = Map(ysize, xsize)
        self.actorGrid = Grid(ysize, xsize)
        self.player = self.add_player(player)
        self.monsters = self.add_monsters()

    def round(self, inkey):
        """one game round starting with player action then monster actions"""
        # player input
        if inkey in ['w', 's', 'a', 'd']:
            self.player.move(inkey)
        if inkey == ">" and self.player.y == self.map.next[0] and self.player.x == self.map.next[1]:
            self.__init__(self.map.ysize, self.map.xsize, self.player)

        # monster turns
        for mon in self.monsters:
            mon.moveCloser()

    def add_player(self, player=None):
        """creates player at start and updates position when moving level"""
        y, x = self.map.rand_inside_point()
        if player:
            player.y = y
            player.x = x
            self.actorGrid[y][x] = player.marker
        return player if player else Player(self, y, x)

    def add_monsters(self):
        """adds monsters to game"""
        mons = []
        for i in range(random.randint(2, 5)):
            y, x = self.map.rand_inside_point()
            mons.append(Monster(self, y, x))
        return mons

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

