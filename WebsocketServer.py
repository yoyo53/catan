import asyncio
import websockets


class WebsocketServer:
    def __init__(self, port):
        self.port = port
        self.clients = []

    async def handler(self, websocket, path):
        print("WebSocket client connected")
        self.clients.append(websocket)
        await asyncio.Future()

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
            await asyncio.sleep(1)

