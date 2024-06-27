import random
import string
from components.Response import Response
from components.ErrorMessage import ErrorMessage

class Lobby:
    def __init__(self):
        self.lobby_id = self.generate_lobby_id(4)
        self.clients = {}
        self.status = "waiting"
        
    def generate_lobby_id(self,length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def join_lobby(self, client_id):
        if len(self.clients) >= 4:
            error = ErrorMessage(0, "Maximum players in this lobby")
            return error.to_json()
    
        if(self.status != "waiting"):
            error = ErrorMessage(0, "Lobby not available, game already started")
            return error.to_json()

        player_number = "player_" + str(len(self.clients) + 1)
        self.clients[player_number] = client_id
        response = Response(1, "success")

        
        return response.to_json()

class LobbyManager:
    def __init__(self):
        self.lobbies = []

    def create_lobby(self):
        lobby = Lobby()
        self.lobbies.append(lobby)
        return lobby.lobby_id

    def get_lobby(self, lobby_id):
        for lobby in self.lobbies:
            if lobby.lobby_id == lobby_id:
                return lobby
        return None
