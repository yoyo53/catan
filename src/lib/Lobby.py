import random

class Lobby:
    def __init__(self):
        self.status = "waiting"
        self.game = None
        self.turn_order = []
        self.players = {}
                    
    
