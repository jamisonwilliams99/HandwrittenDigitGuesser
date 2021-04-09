class Point:
    def __init__(self, grid_coord):
        self.grid_coord = grid_coord

class Grid:
    def __init__(self):
        self.pts = dict()

    def add_point(self, grid_coord):
        self.pts[grid_coord] = Point(grid_coord)

    def access_point(self, grid_coord):
        return self.pts[grid_coord]


