import random
import string
import sys
from components.Response import Response, ErrorMessage

sys.path.append('..')
#from lib import Game, Player
#from lib.map import Map, Tile
from components.ClassGameLogic.GameLogic import GameServ, PlayerServ

class Lobby:
    def __init__(self):
        self.lobby_id = self.generate_lobby_id(4)
        self.clients = {}
        self.status = "waiting"
        self.game = None
        
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
    
    def start_game(self):
        self.game = GameServ()
        for client in self.clients.values():
            self.game.players.append(PlayerServ(client))

        return self.game.to_json()
            
        
        
    def cycle_player(self):
        #should not happen, but just in case
        if len(self.turn_order) != 0:
            self.turn_order.clear()

        turn_order = list(range(1, len(self.clients) + 1))
        random.shuffle(turn_order)

        for client_id, order in zip(self.clients.values(), turn_order):
            self.turn_order.append((client_id, order))

        print(self.turn_order)

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
    
    def get_lobby_by_client(self, client_id):
        for lobby in self.lobbies:
            if client_id in lobby.clients.values():
                return lobby
        return None
