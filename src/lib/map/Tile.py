from lib.map.Edge import Edge
from lib.map.Corner import Corner
from typing import List

class Tile:
    def __init__(self, x, y, type = "", number=0):
        self.type = type
        self.number = number
        # Coordinates of the center of the tile
        self.x = x
        self.y = y

        self.corners : List[Corner] = [] # x6
        self.edges : List[Edge] = [] # x6

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.x == other.x and self.y == other.y
        return False
    
    def __repr__(self) -> str:
        return f"Tile({self.x}, {self.y}) : Corner => [{self.corners}] | Edges : => [{self.edges}]\n\n"    