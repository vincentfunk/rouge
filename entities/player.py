from entities.creature import Creature


class Player(Creature):
    def __init__(self, game, y, x):
        super().__init__(game, y, x)
        self.marker = '@'
        self.health = 10
        self.damage = 3

    def die(self):
        """player died means game over"""
        raise DeadError("YOU DIED")


class DeadError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

