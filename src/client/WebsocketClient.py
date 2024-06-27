import websocket

class WebsocketClient:
    def __init__(self, url, message_queue):
        self.url = url
        self.message_queue = message_queue
        self.ws = websocket.WebSocketApp(
            url, 
            on_open=self.on_open, 
            on_message=self.on_message, 
            on_error=self.on_error, 
            on_close=self.on_close
        )

    def on_open(self, ws):
        print("WebSocket client connected")

    def on_error(self, ws, error):
        print(f"WebSocket client error: {error}")
        self.ws.close()

    def on_close(self, ws):
        print("WebSocket client disconnected")

    def on_message(self, ws, message):
        print(f"Received message: {message}")
        self.message_queue.put(message)

    def start(self):
        self.ws.run_forever()

    def send(self, message):
        self.ws.send(message)
