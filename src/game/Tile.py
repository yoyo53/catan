class Tile:
    def __init__(self, type, number, x, y, z):
        self.type = type
        self.number = number
        self.x = x
        self.y = y
        self.z = z
    
    def getType(self):
        return self.type
    
    def getNumber(self):
        return self.number
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getZ(self):
        return self.z
    
    def __repr__(self):
        return f"Hex({self.x}, {self.y}, {self.z}, {self.type}, {self.number})"
