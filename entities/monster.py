from entities.creature import Creature
from random import randint


class Monster(Creature):
    def __init__(self, game, y, x):
        super().__init__(game, y, x)
        self.marker = 'Z'
        self.health = randint(3, 5)
        self.damage = 2

    def move_closer(self):
        """move closer to the player with a bit of randomness"""
        super().move(self.closer_direction(self, self.game.player))

    def closer_direction(self, e1, e2):
        """1  3
            e2
           6  8"""
        if e1.y <= e2.y and e1.x <= e2.x:
            return "s" if randint(0, 1) else "d"
        elif e1.y <= e2.y and e1.x > e2.x:
            return "s" if randint(0, 1) else "a"
        elif e1.y > e2.y and e1.x <= e2.x:
            return "w" if randint(0, 1) else "d"
        else:
            return "w" if randint(0, 1) else "a"

    def die(self):
        """remove this monster from all locations"""
        self.game.actorGrid[self.y][self.x] = ' '
        self.game.monsters.remove(self)
        # add death text output


