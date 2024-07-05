import sys
sys.path.append('..')
from lib.Lobby import Lobby

class ClientLobby(Lobby):
    def __init__(self):
        super().__init__()
        
    def from_json(self, json):
        self.lobby_id = json["lobby_id"]
        self.players = json["players"]
        self.status = json["status"]


        

    def __repr__(self) -> str:
        return super().__repr__() + f"lobby_id: {self.lobby_id}, players: {self.players}, status: {self.status}"
        
    
