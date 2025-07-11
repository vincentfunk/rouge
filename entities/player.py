from entities.creature import Creature


class Player(Creature):
    def __init__(self, game, y, x):
        super().__init__(game, y, x)
        self.marker = '@'
        # self.game.actorGrid[y][x] = self.marker
        self.health = 10

