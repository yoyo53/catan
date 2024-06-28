import asyncio
import websockets
import json
from components.Exceptions import Exceptions


class WebsocketServer:
    def __init__(self, port):
        self.port = port
        self.clients = []

    async def handler(self, websocket):
        print("WebSocket client connected")
        self.clients.append(websocket)
        while True:
            message = await websocket.recv()
            print("Received message", message)
            response = self.handle_message(message)
            print("response : ", response)

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
            for client in self.clients:
                try:
                    await client.send("ping")
                except websockets.exceptions.ConnectionClosed:
                    print("ws client disconnected")
                    self.clients.remove(client)
                    break
            await asyncio.sleep(20)

    def handle_message(self,message):
        try:
            request = json.loads(message)
            message_type = request['type']
            match(message_type):
                case "create_lobby":
                    print("create lobby here")
                case _:
                    print("to determine")
                
        except (json.JSONDecodeError, KeyError):
            e = Exceptions(0,"Invalid json")
            return e.to_json()



if __name__ == "__main__":
    server = WebsocketServer(8765)
    server.start()