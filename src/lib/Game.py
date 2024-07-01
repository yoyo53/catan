import random
from lib.map.Map import Map
from lib.Dice import Dice


class Game:
    def __init__(self):
        self.players = []
        self.current_player = 0
        self.map = Map()
        self.dice = Dice()
        self.log = []
        self.robbertile = None # Tile where the robber is

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def distribute_resources(self, sumroll : int):
        for tile in self.map.tiles:
            if tile.number == sumroll:
                if tile != self.robbertile:
                    for corner in tile.corners:
                        for player in self.players:
                            if corner.building is not None and corner.building.owner == player:
                                resource = tile.resource
                                if corner.building.type == "settlement":
                                    player.resources[resource] += 1
                                    self.log(f"Player {player} received 1 {resource}")
                                elif corner.building.type == "city":
                                    player.resources[resource] += 2
                                    self.log(f"Player {player} received 1 {resource}")

    def move_robber_and_steal(self, player, tile):
        self.robbertile = tile
        self.log(f"Player {player} moved the robber to tile {tile}")
        playerstealeable = []
        for vertex in tile.vertices:
            for building in vertex.buildings:
                if building is not None and building.owner != player:
                    playerstealeable.append(building.owner)
        if len(playerstealeable) > 0:
            chosenplayer = self.choose_a_player_to_steal(playerstealeable)
            resource = random.choice([res for res, count in chosenplayer.resources.items() if count > 0]) # TO Verify here
            chosenplayer.resources[resource] -= 1
            player.resources[resource] += 1
            self.log(f"Player {player} stole 1 {resource} from player {chosenplayer}")


    def choose_a_player_to_steal(playerstealeable):
        return random.choice(playerstealeable) # for now we just steal random player in the list, CHANGE THIS here