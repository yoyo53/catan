class Corner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = [] # x3 max - x2 min
        self.tiles = [] # x3 max - x1 min
        self.building = None
    
    def __eq__(self, other):
        if isinstance(other, Corner):
            return self.x == other.x and self.y == other.y
        return False
    
    def __lt__(self, other):
        if isinstance(other, Corner):
            if self.x < other.x:
                return True
            elif self.x == other.x:
                return self.y < other.y
        return False
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def to_json(self):
        return {
            "x": self.x,
            "y": self.y
        }
        
    def from_json(self, json):
        self.x = json['x']
        self.y = json['y']
        return self