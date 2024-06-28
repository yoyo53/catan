from Edge import Edge
from Corner import Corner

class Tile:
    def __init__(self, x, y, type = "", number=0):
        self.type = type
        self.number = number
        # Coordinates of the center of the tile
        self.x = x
        self.y = y

        self.corners = [] # x6
        self.edges = [] # x6

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.x == other.x and self.y == other.y
        return False

        

