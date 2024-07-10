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
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.GREEN = (0,255,0)
        self.PURPLE = (128,0,128)
        
    def get_color(self, tile_type):
        colors = {
            'brick': self.BRICK,
            'desert': self.DESERT,
            'ore': self.ORE,
            'wood': self.WOOD,
            'sheep': self.SHEEP,
            'wheat': self.WHEAT,
            1: self.RED,
            2: self.BLUE,
            3: self.GREEN,
            4: self.PURPLE
        }
        return colors.get(tile_type)
        
