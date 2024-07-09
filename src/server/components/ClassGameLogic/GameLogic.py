import sys
#sys.path.append('..')

from lib.map.Map import Map
from lib.map.Tile import Tile
from lib.Game import Game
from lib.Player import Player

class TileServ(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "number": self.number
        }


class MapServ(Map):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def createTile(self, x, y):
        return TileServ(x, y)

    def to_json(self):
        return {
            "tiles": [tile.to_json() for tile in self.tiles]
        }

class GameServ(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map = MapServ()

    def map_to_json(self):
        return self.map.to_json()
    
    def to_json(self):
        return {
            "players": [player.to_json() for player in self.players],
            "map": self.map_to_json()
        }
    
class PlayerServ(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    #def to_json(self):
    #    return {
    #        "name": self.name,
    #        "resources": self.resources,
    #    #    "buildings": self.buildings,
    #    #    "roads": self.roads,
    #        "victory_points": self.points,
    #        "largest_army": self.largest_army,
    #        "longest_road": self.longest_road,
    #    }
    
    def __eq__(self, other):
        if isinstance(other, PlayerServ):
            return self.name == other.name
        return False