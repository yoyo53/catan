from lib.map.Map import Map
from lib.map.Tile import Tile
from lib.map.Corner import Corner
from lib.map.Edge import Edge

from lib.Dice import Dice
from lib.Player import Player
from lib.Building import Building
from lib.Road import Road

from typing import List
import random


class Game:
    def __init__(self):
        self.players : List[Player] = []
        self.current_player = 0
        self.map = Map()
        self.dice = Dice()
        self.log = []

        self.buildings = []
        self.roads = []

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
                                resource = tile.type
                                if corner.building.type == "settlement":
                                    player.resources[resource] += 1
                                    self.log(f"Player {player} received 1 {resource}")
                                elif corner.building.type == "city":
                                    player.resources[resource] += 2
                                    self.log(f"Player {player} received 1 {resource}")

    def move_robber_and_steal(self, player, tile : Tile):
        def choose_a_player_to_steal(playerstealeable):
            return random.choice(playerstealeable) # for now we just steal random player in the list, CHANGE THIS here

        self.robbertile = tile
        self.log(f"Player {player} moved the robber to tile {tile}")
        playerstealeable = []
        for corner in tile.corners:
            if corner.building is not None and corner.building.owner != player:
                playerstealeable.append(corner.building.owner)
        if len(playerstealeable) > 0:
            chosenplayer = choose_a_player_to_steal(playerstealeable)
            resource = random.choice([res for res, count in chosenplayer.resources.items() if count > 0]) # TO Verify here
            chosenplayer.resources[resource] -= 1
            player.resources[resource] += 1
            self.log(f"Player {player} stole 1 {resource} from player {chosenplayer}")
    

    def build_settlement(self, player, corner) -> bool:
        def canbuild(player, corner : Corner) -> bool:
            for edge in corner.edges:
                if edge.road is not None and edge.road.owner == player:
                    for c in edge.corners:
                        if c.building is not None:
                            return False
                    return True
            return False
        
        if canbuild(player, corner):
            player.resources["brick"] -= 1
            player.resources["wood"] -= 1
            player.resources["sheep"] -= 1
            player.resources["wheat"] -= 1
            self.map.buildings.append(Building("settlement", corner, player))
            self.log(f"Player {player} built a settlement at {corner}")
            return True
        return False
    

    def check_build_road(self, player, edge : Edge) -> bool:      
        if edge.road is None:
            #if edge.corners in [c for r in player.roads for c in r.edge.corners]: # TO VERIFY HERE
            player.resources["brick"] += 1
            player.resources["wood"] += 1 
            if (player.resources["brick"] >= 1) and (player.resources["wood"] >= 1):
                return True
        return False
    
    def build_city(self, player, corner) -> bool:
        if corner.building is not None and corner.building.owner == player and corner.building.type == "settlement":
            player.resources["wheat"] -= 2
            player.resources["ore"] -= 3
            corner.building.change_to_city()
            self.log(f"Player {player} built a city at {corner}")
            return True
        return False
    
    def count_longest_road(self, player): # TO VERIFY HERE ===>  COPILOT (HARD)
        def dfs(player, edge, visited, length):
            visited.add(edge)
            length += 1
            max_length = length
            for c in edge.corners:
                for e in c.edges:
                    if e.road is not None and e.road.owner == player and e not in visited:
                        max_length = max(max_length, dfs(player, e, visited, length))
            visited.remove(edge)
            return max_length
        
        visited = set()
        max_length = 0
        for edge in self.map.edges:
            if edge.road is not None and edge.road.owner == player:
                max_length = max(max_length, dfs(player, edge, visited, 0))
        return max_length
    
def main():
    game = Game()
    game.players.append(Player("Player 1"))
    game.players.append(Player("Player 2"))
    game.players.append(Player("Player 3"))
    game.players.append(Player("Player 4"))

    print(game.map.tiles)

if __name__ == "__main__":
    main()