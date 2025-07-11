from entities.creature import Creature
from random import randint


class Monster(Creature):
    def __init__(self, game, y, x):
        super().__init__(game, y, x)
        self.marker = 'Z'
        # self.game.actorGrid[y][x] = self.marker
        self.health = randint(3, 5)

    def move_closer(self):
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

