class Room:
    def __init__(self, y1, x1, y2, x2):
        self.ylen = y2 - y1
        self.xlen = x2 - x1
        self.ymin = y1
        self.ymax = y2
        self.xmin = x1
        self.xmax = x2
        self.topl = (y1, x1)
        self.topr = (y1, x2)
        self.botl = (y2, x1)
        self.botr = (y2, x2)
        self.cords = [self.topl, self.topr, self.botl, self.botr]

    def is_inside(self, point):
        """checks if a cord tuple is inside this room sides included"""
        return True if self.ymin <= point[0] <= self.ymax and self.xmin <= point[1] <= self.xmax else False

    def is_close(self, point):
        """checks if a cord tuple is inside or within 1 space this room"""
        return True if self.ymin - 1 <= point[0] <= self.ymax + 1 and self.xmin - 1 <= point[1] <= self.xmax + 1 else False

    def all_points(self):
        """generator for all points of the room edges included"""
        for y in range(self.ymin, self.ymax + 1):
            for x in range(self.xmin, self.xmax + 1):
                yield (y, x)

    def allInsidePoints(self):
        """generator for all points of the room edges excluded"""
        for y in range(self.ymin + 1, self.ymax):
            for x in range(self.xmin + 1, self.xmax):
                yield (y, x)
