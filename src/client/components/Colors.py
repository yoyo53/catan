class Colors:
    def __init__ (self):
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.WOOD = (34,139,34)
        self.WHEAT = (255,223,0)
        self.SHEEP = (50,205,50)
        self.ORE = (128,128,128)
        self.BRICK = (139,69,19)
        self.DESERT = (210,180,149)
        
    def get_color(self, tile_type):
        colors = {
            'brick': self.BRICK,
            'desert': self.DESERT,
            'ore': self.ORE,
            'wood': self.WOOD,
            'sheep': self.SHEEP,
            'wheat': self.WHEAT,
        }
        return colors.get(tile_type)