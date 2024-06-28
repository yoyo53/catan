class Map:
    #attributes are hardcoded because they are the same for every game
    def __init__ (self):
        self.tiles = [] # List of tiles on the map
        self.edges = [] # List of edges on the map
        self.corners = [] # List of corners on the map
        
        self.buildings = [] # List of buildings on the map
        self.roads = []
        self.robbertile = None

        self.array_number = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        self.array_type = {
            "brick": 3,
            "desert": 1,
            "ore": 3,
            "wood": 4,
            "sheep": 4,
            "wheat": 4
        }
