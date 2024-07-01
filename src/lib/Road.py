from Player import Player
from map.Edge import Edge

class Road:
    def __init__(self, owner : Player, edge : Edge):
        self.owner = owner
        self.edge = edge

        edge.road = self

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Road):
            return self.owner == value.owner and self.edge == value.edge
        return False