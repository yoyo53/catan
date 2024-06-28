class Edge:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.corners = [] # x2
        self.tiles = [] # x2 max
        self.road = None
