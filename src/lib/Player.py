class Player:
    def __init__(self, name):
        self.name = name
        self.resources = { # FOR TESTING PURPOSES
            "wood": 100,
            "brick": 100,
            "sheep": 100,
            "wheat": 100,
            "ore": 100
        }
        self.buildings = []
        self.roads = []
        self.dev_cards = []

        self.points = 0
        self.largest_army = False
        self.longest_road = False

    def update(self, resources = None, buildings = None, roads = None, dev_cards = None, points = None, largest_army = None, longest_road = None):
        if resources is not None:
            self.resources = resources
        if buildings is not None:
            self.buildings = buildings
        if roads is not None:
            self.roads = roads
        if dev_cards is not None:
            self.dev_cards = dev_cards
        if points is not None:
            self.points = points
        if largest_army is not None:
            self.largest_army = largest_army
        if longest_road is not None:
            self.longest_road = longest_road
    
    def json_to_buldings(self, json):
        pass
    
    def to_json(self):
        return {
            "name": self.name,
            "resources": self.resources,
            "roads": self.roads,
        #    "buildings": self.buildings,
            "victory_points": self.points,
            "largest_army": self.largest_army,
            "longest_road": self.longest_road,
        }
        
    def from_json(self, json):
        self.name = json['name']
        self.resources = json['resources']
        #self.roads = json['roads']
        #self.buildings = json['buildings']
        self.points = json['victory_points']
        self.largest_army = json['largest_army']
        self.longest_road = json['longest_road']