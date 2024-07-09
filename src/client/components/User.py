from threading import Thread
from WebsocketClient import WebsocketClient
import time
import json
from queue import Queue

from game.ClientGame import ClientGame
from game.ClientLobby import ClientLobby

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
        self.lobby = None
        self.game = None
        self.my_turn = None

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
                    self.game = ClientGame(self.ui, response['data']['jsondata'])
                    self.ui.change_state("game_started")
                    self.game.turn_order = response['data']['turn_order']
                    for player_name, order in self.game.turn_order:
                        if player_name == self.username:
                            self.my_turn = order
                case "end_turn":
                    self.game.next_turn()

                case _:
                    print("Unknown message type")
                    print(response)

