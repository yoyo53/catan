import random
import string
import sys
from components.Response import Response, ErrorMessage

sys.path.append('..')
from components.ClassGameLogic.GameLogic import GameServ, PlayerServ
from lib.Lobby import Lobby

class LobbyServer(Lobby):
    def __init__(self):
        super().__init__()
        self.lobby_id = self.generate_lobby_id(4)
    
    def start_game(self):
        self.game = GameServ()
        for client in self.players.values():
            self.game.players.append(PlayerServ(client))
        return self.game.to_json()
    
    def generate_lobby_id(self,length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def join_lobby(self, client_id):
        if len(self.players) >= 4:
            error = ErrorMessage(0, "Maximum players in this lobby")
            return error.to_json()
    
        if(self.status != "waiting"):
            error = ErrorMessage(0, "Lobby not available, game already started")
            return error.to_json()

        player_number = "player_" + str(len(self.players) + 1)
        self.players[player_number] = client_id
        response = Response(1, "success")
        
        return response.to_json()
    
    def to_json(self):
        return {
            "lobby_id": self.lobby_id,
            "players": self.players,
            "status": self.status,
        }

class LobbyManager:
    def __init__(self):
        self.lobbies = []

    def create_lobby(self):
        lobby = LobbyServer()
        self.lobbies.append(lobby)
        return lobby.lobby_id

    def get_lobby(self, lobby_id):
        for lobby in self.lobbies:
            if lobby.lobby_id == lobby_id:
                return lobby
        return None
    
    def get_lobby_by_client(self, client_id):
        for lobby in self.lobbies:
            if client_id in lobby.players.values():
                return lobby
        return None
