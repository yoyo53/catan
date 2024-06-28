from threading import Thread
from WebsocketClient import WebsocketClient
import time
import json
from queue import Queue

SERVER_URL = "ws://127.0.0.1:8765"

class User:
    def __init__(self, username, ui):
        self.message_queue = Queue()
        self.client = WebsocketClient(SERVER_URL, self.message_queue)
        self.username = username
        self.ui = ui
        Thread(target=self.client.start).start()
        time.sleep(0.5)
        request = json.dumps({"type": "greeting", "data": {"username": self.username}})
        self.client.send(request)
        self.hosted_games = []

    def create_lobby(self):
        request = json.dumps({"type": "create_lobby", "data": {}})
        self.client.send(request)

    def join_lobby(self,lobby_id):
        request = json.dumps({"type": "join_lobby", "data": {"lobby_id":lobby_id}})
        self.client.send(request)
    
    def handle_messages(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            if(message == "ping"): return # send pong ?
            response = json.loads(message)
            message_type = response['data']['type']
            match message_type:
                case "create_lobby":
                    lobby_id = response['data']['lobby_id']
                    self.hosted_games.append(lobby_id)
                    self.ui.display_lobby(lobby_id, {"player_1": self.username})
                    self.ui.display_start_button()
                case "join_lobby":
                    lobby_id = response['data']['lobby_id']
                    players = response['data']['players']
                    self.ui.display_lobby(lobby_id, players)
                    if(lobby_id in self.hosted_games): self.ui.display_start_button() #if user is host, get the start button
                case "error":
                    error_message = response['data']['error_message']
                    previous_screen, previous_buttons = self.ui.screen_copy()  # Take a snapshot of the current screen and buttons
                    self.ui.display_error(error_message, previous_screen, previous_buttons)
                case _:
                    print("Unknown message type")
