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