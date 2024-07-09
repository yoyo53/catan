import sys
import random
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

    def generate_turn_order(self):
        #should not happen, but just in case
        if len(self.turn_order) != 0:
            self.turn_order.clear()

        for player in self.players:
            print(player.name)

        turn_order = list(range(1, len(self.players) + 1))
        random.shuffle(turn_order) #ex : [1, 3, 2, 4]

        for player, order in zip(self.players, turn_order):
            self.turn_order.append((player.name, order))
    
    def get_client_turn(self, client):
        for player_name, order in self.turn_order:
            if player_name == client:
                return order
        return None

    
class PlayerServ(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def to_json(self):
        return {
            "name": self.name,
            "resources": self.resources,
            "buildings": self.buildings,
            "roads": self.roads,
            "victory_points": self.points,
            "largest_army": self.largest_army,
            "longest_road": self.longest_road,
        }
    
    def __eq__(self, other):
        if isinstance(other, PlayerServ):
            return self.name == other.name
        return False