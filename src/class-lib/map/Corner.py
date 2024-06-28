class Corner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edge = [] # x3 max - x2 min
        self.tiles = [] # x2 max - x1 min