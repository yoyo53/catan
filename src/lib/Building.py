from lib.Player import Player
from lib.map.Corner import Corner

class Building:
    def __init__(self, type : str, corner : Corner, owner : Player):
        self.type = type # "settlement" or "city"
        self.owner = owner # Player who owns the building
        
        # Corner bind
        self.corner = corner
        corner.building = self

        # Player bind
        owner.buildings.append(self)

    def __repr__(self) -> str:
        return f"{self.type} at {self.corner} owned by {self.owner}"
    
    def __eq__(self, other):
        if isinstance(other, Building):
            return self.type == other.type and self.corner == other.corner and self.owner == other.owner
        return False
    
    def change_to_city(self):
        self.type = "city"