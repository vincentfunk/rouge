class Hall:
    def __init__(self, r1, r2, start, end, corner=None):
        self.room1 = r1
        self.room2 = r2
        self.start = start
        self.end = end
        self.corner = corner

    def all_points(self):
        """list for all points of the hall"""
        if self.corner is None:
            return self.straight_points(self.start, self.end)
        else:
            return self.straight_points(self.start, self.corner) + self.straight_points(self.corner, self.end)

    def straight_points(self, p1, p2):
        """return all list of points between two points ends included
            given you know the line is horizontal or vertical"""
        points = []
        # in order to keep order of points correct iterate in reverse rather than switching points
        # horizontal
        if p1[0] == p2[0]:
            y = p1[0]
            if p1[1] < p2[1]:
                for x in range(p1[1], p2[1] + 1):
                    points.append((y, x))
            else:
                for x in range(p1[1], p2[1] - 1, -1):
                    points.append((y, x))
        # vertical
        elif p1[1] == p2[1]:
            x = p1[1]
            if p1[0] < p2[0]:
                for y in range(p1[0], p2[0] + 1):
                    points.append((y, x))
            else:
                for y in range(p1[0], p2[0] - 1, -1):
                    points.append((y, x))
        else:
            raise ValueError("Points not horizontal or vertical")
        return points

