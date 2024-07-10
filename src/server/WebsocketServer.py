import asyncio
import websockets
import json
import random
import string
from components.Response import Response,ErrorMessage
from components.LobbyManager import LobbyManager
import sys

sys.path.append('..')

from lib.map.Corner import Corner
from lib.Building import Building
from lib.map.Edge import Edge
from lib.Road import Road

class WebsocketServer:
    def __init__(self, port):
        self.port = port
        self.clients = {}  # Dictionary of {client_id: ws} with client_id = username + # + random_id
        self.lobby_manager = LobbyManager()

    async def handler(self, ws):
        print("WebSocket client connected")
        greeting = await ws.recv()
        await self.register_client(greeting, ws)
        while True:
            message = await ws.recv()
            response = await self.handle_message(message,ws)
            await ws.send(response)

    async def start_async(self):
        server = await websockets.serve(self.handler, "0.0.0.0", self.port)
        print("WebSocket server started")
        await self.run()
        await server.close()
        print("WebSocket server closed")

    def start(self):
        asyncio.run(self.start_async())

    async def run(self):
        while True:
            for client, ws in self.clients.items():
                try:
                    await ws.send("ping")
                except websockets.exceptions.ConnectionClosed:
                    print("ws client disconnected")
                    del self.clients[client]
                    break
            await asyncio.sleep(20)

    async def handle_message(self, message, ws):
        try:
            request = json.loads(message)
            message_type = request['type']
            client = self.get_client(ws)
            match message_type:
                case "create_lobby":
                    return self.create_lobby(client)
                case "join_lobby":
                    return await self.join_lobby(request,client)
                case "start_game":
                    return await self.start_game(client)
                case "check_permission":
                    return await self.check_permission(request,client)
                case "end_turn":
                    return await self.end_turn(client) 
                case _:
                    error = ErrorMessage(0,"Unknown message type")
                    return error.to_json()
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Exception: {e}")
            error = ErrorMessage(0, "Invalid JSON")
            return error.to_json()


    async def register_client(self, greeting, ws):
        message = json.loads(greeting)
        username = message['data']['username']
        id = self.generate_client_id(4)
        client_id = username + "#" + id
        self.clients[client_id] = ws
        response = Response(1, "greeting", client_id=client_id)
        await ws.send(response.to_json())
    
    def get_client(self,ws):
        for client_id in self.clients:
            if(self.clients[client_id] == ws):
                return client_id
    
    def generate_client_id(self, length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create_lobby(self, client):
        lobby_id = self.lobby_manager.create_lobby()
        lobby = self.lobby_manager.get_lobby(lobby_id)
        lobby.join_lobby(client)
        response = Response(1, "create_lobby",lobby=lobby.to_json())
        return response.to_json()
    
    async def join_lobby(self,request, client_id):
        lobby_id = request['data']['lobby_id']
        lobby = self.lobby_manager.get_lobby(lobby_id) 
        ws = self.clients[client_id]
        if(lobby is None):
            response = ErrorMessage(0,"Lobby doesn't exist")
            return response.to_json()
        
        join_attempt = json.loads(lobby.join_lobby(client_id)) 
        if(join_attempt['status'] == 0):
            return json.dumps(join_attempt)

        #to notice all clients that someone just joined the lobby
        response = Response(1, "join_lobby",lobby=lobby.to_json())
        for client_id in lobby.players.values():
            ws = self.clients[client_id]
            await ws.send(response.to_json())
        return response.to_json()
    
    async def start_game(self,client):
        lobby = self.lobby_manager.get_lobby_by_client(client)
        if(lobby.players['player_1'] != client):
            response = ErrorMessage(0,"You are not the host")
            return response.to_json()
        
        jsondata = lobby.start_game()
        lobby.game.generate_turn_order()
        response = Response(666,"game_start",jsondata = jsondata, turn_order=lobby.game.turn_order)
        for client_id in lobby.players.values():
            ws = self.clients[client_id]
            await ws.send(response.to_json())
        return response.to_json()
    
    def check_permission(self, request, client):
        request_data_action = request['data']['action']
        match request_data_action:
            case "build_road":
                return self.build_road(request,client)
            case "build_settlement":
                return self.build_settlement(request,client)
            case "upgrade_settlement":
                return self.upgrade_settlement(request,client)
            case _:
                error = ErrorMessage(0,"Unknown action")
                return error.to_json()

    async def build_road(self, request, client):
        lobby_id = request['data']['lobby_id']
        lobby = self.lobby_manager.get_lobby(lobby_id)
        corner1 = Corner(*request['data']['edge']['corner1'])
        corner2 = Corner(*request['data']['edge']['corner2'])
        
        for c in lobby.game.map.corners:
            if c == corner1:
                corner1 = c
            if c == corner2:
                corner2 = c
        edge = Edge(corner1,corner2)
        for e in lobby.game.map.edges:
            if e == edge:
                edge = e
        
        player_name = request['data']['player']
        for p in lobby.game.players:
            if p.name == player_name:
                player = p
        player.resources["bricks"] = 10
        player.resources["wood"] = 10
        if (lobby.game.check_build_road(player, edge)):
            lobby.game.map.roads.append(Road(player, edge))
            player.resources["brick"] -= 1
            player.resources["wood"] -= 1
            response = Response(1, "road_created", edge=edge.to_json(), player=player.to_json())
            for client_id in lobby.players.values():
                ws = self.clients[client_id]
                await ws.send(response.to_json())
        else:
            response = ErrorMessage(0,"You can't build a road here")
        return response.to_json()
    
    async def build_settlement(self, request, client):
        lobby_id = request['data']['lobby_id']
        lobby = self.lobby_manager.get_lobby(lobby_id)
        corner = Corner(*request['data']['corner'])
        for c in lobby.game.map.corners:
            if c == corner:
                corner = c
        player_name = request['data']['player']
        for p in lobby.game.players:
            if p.name == player_name:
                player = p
        if (lobby.game.check_build_settlement(player, corner)):
            lobby.game.map.buildings.append(Building("settlement", corner,player))
            player.resources["brick"] -= 1
            player.resources["wood"] -= 1
            player.resources["sheep"] -= 1
            player.resources["wheat"] -= 1
            response = Response(1, "settlement_created", corner=corner.to_json(), player=player.to_json())
            for client_id in lobby.players.values():
                ws = self.clients[client_id]
                await ws.send(response.to_json())
        else:
            response = ErrorMessage(0,"You can't build a settlement here")
        return response.to_json()
    
    async def upgrade_settlement(self, request, client):
        lobby_id = request['data']['lobby_id']
        lobby = self.lobby_manager.get_lobby(lobby_id)
        corner = Corner(*request['data']['corner'])
        for c in lobby.game.map.corners:
            if c == corner:
                corner = c
        player_name = request['data']['player']
        for p in lobby.game.players:
            if p.name == player_name:
                player = p
        if (lobby.game.check_upgrade_settlement(player, corner)):
            for b in lobby.game.map.buildings:
                if b.corner == corner and b.owner == player:
                    b.type = "city"
            player.resources["wheat"] -= 2
            player.resources["ore"] -= 3
            response = Response(1, "settlement_upgraded", corner=corner.to_json(), player=player.to_json())
            for client_id in lobby.players.values():
                ws = self.clients[client_id]
                await ws.send(response.to_json())
        else:
            response = ErrorMessage(0,"You can't upgrade a settlement here")
        return response.to_json()
    
    async def end_turn(self,client):
        lobby = self.lobby_manager.get_lobby_by_client(client)
        client_turn = lobby.game.get_client_turn(client)
        if(lobby.game.current_player_turn != client_turn):
            response = ErrorMessage(0,"Not your turn")
            return response.to_json()
        
        lobby.game.next_turn()
        response = Response(1,"end_turn")
        for client_id, ws in self.clients.items():
            if client_id != client:
                await ws.send(response.to_json())
        return response.to_json()
        

if __name__ == "__main__":
    server = WebsocketServer(8765)
    server.start()
