import random

class Lobby:
    def __init__(self):
        self.status = "waiting"
        self.game = None
        self.turn_order = []
        self.players = {}
                    
    def generate_turn_order(self):
        #should not happen, but just in case
        if len(self.turn_order) != 0:
            self.turn_order.clear()

        turn_order = list(range(1, len(self.players) + 1))
        random.shuffle(turn_order)

        for client_id, order in zip(self.players.values(), turn_order):
            self.turn_order.append((client_id, order))

        print(self.turn_order)
