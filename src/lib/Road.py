from lib.Player import Player
from lib.map.Edge import Edge

class Road:
    def __init__(self, owner : Player, edge : Edge):
        self.owner = owner
        self.edge = edge
        edge.road = self

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Road):
            return self.owner == value.owner and self.edge == value.edge
        return False
    
    def __repr__(self) -> str:
        return f"Road({self.owner}, {self.edge})"