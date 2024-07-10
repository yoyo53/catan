from threading import Thread
from WebsocketClient import WebsocketClient
import time
import json
from queue import Queue
import sys

sys.path.append('..')


from game.ClientGame import ClientGame
from game.ClientLobby import ClientLobby
from lib.map.Edge import Edge
from lib.map.Corner import Corner
from lib.Building import Building
from lib.Road import Road

SERVER_URL = "ws://127.0.0.1:8765"

class User:
    def __init__(self, username, ui):
        self.message_queue = Queue()
        self.client = WebsocketClient(SERVER_URL, self.message_queue)
        self.username = username
        self.ui = ui
        self.ui.user = self
        Thread(target=self.client.start).start()
        time.sleep(0.5)
        request = json.dumps({"type": "greeting", "data": {"username": self.username}})
        self.client.send(request)
        self.hosted_games = []
        self.game = None
        self.lobby = None
        self.my_turn = None

        self.player = None

    #def get_player(self):
    #    return self.player

    def create_lobby(self):
        request = json.dumps({"type": "create_lobby", "data": {}})
        self.client.send(request)

    def join_lobby(self,lobby_id):
        request = json.dumps({"type": "join_lobby", "data": {"lobby_id":lobby_id}})
        self.client.send(request)

    def start_game(self):
        request = json.dumps({"type": "start_game", "data": {}})
        self.client.send(request)

    def end_turn(self):
        request = json.dumps({"type": "end_turn", "data": {}})
        self.client.send(request)
        
    def build_road(self, edge):
        if (self.game.check_build_road(self.player, edge)):
            print("Building road")
            player = self.player
            request = json.dumps({"type": "check_permission", "data": {"edge": {"corner1": (edge.corners[0].x, edge.corners[0].y), "corner2": (edge.corners[1].x, edge.corners[1].y)}, "player": player.name, "lobby_id": self.lobby.lobby_id, "action": "build_road"}})
            self.client.send(request)

    def build_settlement(self, corner):
        if (self.game.check_build_settlement(self.player, corner)):
            print("Building settlement")
            player = self.player
            request = json.dumps({"type": "check_permission", "data": {"corner": (corner.x, corner.y), "player": player.name, "lobby_id": self.lobby.lobby_id, "action": "build_settlement"}})
            self.client.send(request)

    def upgrade_settlement(self, corner):
        if (self.game.check_upgrade_settlement(self.player, corner)):
            print("Upgrading settlement")
            player = self.player
            request = json.dumps({"type": "check_permission", "data": {"corner": (corner.x, corner.y), "player": player.name, "lobby_id": self.lobby.lobby_id, "action": "upgrade_settlement"}})
            self.client.send(request)
    
    def get_turn_order(self):
        request = json.dumps({"type": "get_turn_order", "data": {}})
        self.client.send(request)
    
    def handle_messages(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            if(message == "ping"): return # send pong ?
            response = json.loads(message)
            message_type = response['data']['type']
            match message_type:
                case "greeting":
                    self.username = response['data']['client_id']
                case "create_lobby":
                    lobby_json = response['data']['lobby']
                    client_lobby = ClientLobby()
                    client_lobby.from_json(lobby_json)
                    self.lobby = client_lobby
                    self.hosted_games.append(self.lobby.lobby_id)
                    self.ui.change_state("lobby")
                case "join_lobby":
                    lobby_json = response['data']['lobby']
                    client_lobby = ClientLobby()
                    client_lobby.from_json(lobby_json)
                    self.lobby = client_lobby
                    self.ui.change_state("lobby")
                case "error":
                    error_message = response['data']['error_message']
                    self.ui.error = error_message
                case "game_start":
                    self.game = ClientGame(self.ui, response['data']['jsondata'], self)
                    self.ui.change_state("game_started")
                    #self.ui.draw_game(self.game)
                    #self.ui.draw_hud(self.game)
                case "road_created":
                    player = self.player
                    player_json = response['data']['player']
                    player.from_json(player_json)
                    edge_json = response['data']['edge']
                    edge_new = Edge.from_json(edge_json)
                    print("Edge receive", edge_new)
                    for edge in self.game.map.edges:
                        if edge.equals_coords(edge_new):
                            print("You find me !")
                            edge_new = edge
                    # TEST PURPOSE ONLY
                    player.color = (255, 0, 0)
                    # TEST PURPOSE ONLY
                    self.game.map.roads.append(Road(player, edge_new))
                    #print(self.game.map.roads)
                case "settlement_created":
                    player = self.player
                    player_json = response['data']['player']
                    player.from_json(player_json)
                    corner_json = Corner.from_json(response['data']['corner'])
                    for corner in self.game.map.corners:
                        if corner == corner_json:
                            my_corner = corner

                    self.game.map.buildings.append(Building("settlement", my_corner, player))

                case "settlement_upgraded":
                    player = self.player
                    player_json = response['data']['player']
                    player.from_json(player_json)
                    corner_json = Corner.from_json(response['data']['corner'])
                    for corner in self.game.map.corners:
                        if corner == corner_json:
                            my_corner = corner

                    for building in self.game.map.buildings:
                        if building.corner == my_corner:
                            building.type = "city"

                case "turn_order":
                    self.game.turn_order = response['data']['turn_order']
                    for player_name, order in self.game.turn_order:
                        if player_name == self.username:
                            self.my_turn = order
                case "end_turn":
                    self.game.next_turn()

                case _:
                    print("Unknown message type")
                    print(response)
