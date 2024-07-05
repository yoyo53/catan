import random
import math
import pygame
import sys

sys.path.append('..')
from lib.Game import Game
from lib.Player import Player
from game.ClientMap import ClientMap

class ClientGame(Game):
    def __init__(self, UI, jsongame):
        super().__init__()
        self.map = ClientMap(UI)
        self.status = "start"
        self.ui = UI
        self.creategame(jsongame)
        self.lobby_id = None

    def creategame(self, json):
        # JSON IN THIS FORMAT :
        #{"players": [{"name": "Ougo#WK5O", "resources": {"wood": 0, "brick": 0, "sheep": 0, "wheat": 0, "ore": 0}, "buildings": [], "roads": [], "victory_points": 0, "largest_army": false, "longest_road": false}], "map": {"tiles": [{"x": -2, "y": -6, "type": "sheep", "number": 3}, {"x": 0, "y": -6, "type": "desert", "number": 0}, {"x": 2, "y": -6, "type": "wood", "number": 8}, {"x": -3, "y": -3, "type": "wheat", "number": 2}, {"x": -1, "y": -3, "type": "sheep", "number": 4}, {"x": 1, "y": -3, "type": "sheep", "number": 11}, {"x": 3, "y": -3, "type": "wood", "number": 8}, {"x": -4, "y": 0, "type": "sheep", "number": 5}, {"x": -2, "y": 0, "type": "ore", "number": 5}, {"x": 0, "y": 0, "type": "wood", "number": 9}, {"x": 2, "y": 0, "type": "brick", "number": 10}, {"x": 4, "y": 0, "type": "wheat", "number": 9}, {"x": -3, "y": 3, "type": "wood", "number": 11}, {"x": -1, "y": 3, "type": "ore", "number": 10}, {"x": 1, "y": 3, "type": "brick", "number": 4}, {"x": 3, "y": 3, "type": "wheat", "number": 6}, {"x": -2, "y": 6, "type": "brick", "number": 3}, {"x": 0, "y": 6, "type": "wheat", "number": 6}, {"x": 2, "y": 6, "type": "ore", "number": 12}]}
        for player in json["players"]:
            self.players.append(Player(player["name"]))

        self.map.updatetile(json["map"])