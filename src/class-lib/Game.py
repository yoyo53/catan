import random
from map.Map import Map
from Dice import Dice


class Game:
    def __init__(self):
        self.players = []
        self.current_player = 0
        self.board = Map()
        self.dice = Dice()
        self.log = []

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def distribute_resources(self, sumroll):
        for tile in self.board.tiles:
            if tile.number == sumroll:
                if tile == self.robber:  # the robber is just a tile ?
                    for vertex in tile.vertices:
                        for player in self.players:
                            for building in vertex.buildings: # they are max 2 buildings on a vertex
                                if building is not None and building.owner == player:
                                    resource = tile.resource
                                    if building.type == "settlement":
                                        player.resources[resource] += 1
                                        self.log(f"Player {player} received 1 {resource}")
                                    elif building.type == "city":
                                        player.resources[resource] += 2
                                        self.log(f"Player {player} received 1 {resource}")

    def move_robber_and_steal(self, player, tile):
        self.robber = tile  # the robber is just a tile ?
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