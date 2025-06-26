from entities.creature import Creature
import random
class Monster(Creature):
    def __init__(self, game, y, x):
        super().__init__(game, y, x)
        self.marker = 'Z'
        self.game.actorGrid[y][x] = self.marker

    def moveCloser(self):
        super().move(self.closerDirect(self, self.game.player))

    def closerDirect(self, e1, e2):
        """1  3
            e2
           6  8"""
        if e1.y <= e2.y and e1.x <= e2.x:
            return "s" if random.randint(0, 1) else "d"
        elif e1.y <= e2.y and e1.x > e2.x:
            return "s" if random.randint(0, 1) else "a"
        elif e1.y > e2.y and e1.x <= e2.x:
            return "w" if random.randint(0, 1) else "d"
        else:
            return "w" if random.randint(0, 1) else "a"