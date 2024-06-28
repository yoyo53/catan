class Tile:
    def __init__(self, type, number, x, y, z):
        self.type = type
        self.number = number
        self.x = x
        self.y = y
        self.z = z

        self.corners = [] # x6
        self.edges = [] # x6

        

