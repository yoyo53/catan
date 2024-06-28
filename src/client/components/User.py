from WebsocketClient import WebsocketClient
from threading import Thread
import time
import json

SERVER_URL = "ws://127.0.0.1:8765"

class User:
    def __init__(self,username):
        self.client = WebsocketClient(SERVER_URL)
        self.username = username
        Thread(target=self.client.start).start()
        time.sleep(0.5)

    def create_lobby(self):
        request = json.dumps({"type":"create_lzzzobby", "data": {"username": self.username}})
        self.client.send(request)
