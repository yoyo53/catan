import asyncio
import websockets
import json
import random
import string
from components.Response import Response
from components.LobbyManager import LobbyManager
from components.ErrorMessage import ErrorMessage

class WebsocketServer:
    def __init__(self, port):
        self.port = port
        self.clients = {}  # Dictionary of {client_id: ws} with client_id = username + # + random_id
        self.lobby_manager = LobbyManager()

    async def handler(self, ws):
        print("WebSocket client connected")
        greeting = await ws.recv()
        self.register_client(greeting, ws)
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
                    await self.join_lobby(request,client)
                    response = Response(1,"information",message="Successfully joined lobby")
                    return response.to_json()
                case "start_game":
                    lobby_id = request['data']['lobby_id']
                    await self.get_turn_order(lobby_id)
                    response = Response(1,"information",message="Game started")
                    return response.to_json()
                case _:
                    error = ErrorMessage(0, "Unknown message type")
                    return error.to_json()
        except (json.JSONDecodeError, KeyError):
            error = ErrorMessage(0, "Invalid JSON")
            return error.to_json()

    def register_client(self, greeting, ws):
        message = json.loads(greeting)
        username = message['data']['username']
        id = self.generate_client_id(4)
        client_id = username + "#" + id
        self.clients[client_id] = ws
    
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
        response = Response(1, "create_lobby",lobby_id=lobby_id)
        return response.to_json()
    
    async def join_lobby(self,request, client):
        lobby_id = request['data']['lobby_id']
        lobby = self.lobby_manager.get_lobby(lobby_id)
        lobby.join_lobby(client)

        #to notice all clients that someone just joined the lobby
        response = Response(1, "join_lobby",lobby_id=lobby_id, players=lobby.clients)
        for client_id in lobby.clients.values():
            ws = self.clients[client_id]
            await ws.send(response.to_json())
        
    async def get_turn_order(self,lobby_id):
        lobby = self.lobby_manager.get_lobby(lobby_id)
        lobby.cycle_player()
        for client_id in lobby.clients.values():
            ws = self.clients[client_id]
            response = Response(1, "turn_order", turn_order=lobby.turn_order)
            await ws.send(response.to_json())
        

if __name__ == "__main__":
    server = WebsocketServer(8765)
    server.start()
