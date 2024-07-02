class Player:
    def __init__(self, name):
        self.name = name
        self.resources = {
            "wood": 0,
            "brick": 0,
            "sheep": 0,
            "wheat": 0,
            "ore": 0
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