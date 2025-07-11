class Creature:
    def __init__(self, game, y, x):
        self.game = game
        self.y = y
        self.x = x
        self.marker = '?'
        self.game.actorGrid[y][x] = self.marker
        self.room = self.currentRoom()

    def move(self, direction):
        """moves entity in a direction
        add checks for other entities adjacent"""
        if direction == 'w':
            target = self.y - 1, self.x
        elif direction == 's':
            target = self.y + 1, self.x
        elif direction == 'a':
            target = self.y, self.x - 1
        elif direction == 'd':
            target = self.y, self.x + 1
        else:
            raise ValueError(type(self), "movement must be wsad")
        if target in self.game.map.valid_moves() and self.game.actorGrid[target[0]][target[1]] == ' ':
            self.game.actorGrid[self.y][self.x] = ' '
            self.game.actorGrid[target[0]][target[1]] = self.marker
            self.y, self.x = target

    def currentRoom(self):
        pass