from components.Button import Button

class ButtonManager:
    def __init__(self, screen, colors):
        self.buttons = []
        self.screen = screen
        self.colors = colors

    def add_button(self, button):
        self.buttons.append(button)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()

    def clear_buttons(self):
        self.buttons = []

    def create_main_menu_buttons(self):
        if len(self.buttons) == 0: # Only create buttons if there are none, ON CREEE PAS DES BOUTONS A CHAQUE FRAME HEIN LUCAS
            create_lobby_button = Button(self.screen, self.colors.WHEAT, 100, 100, 250, 50, "Créer un lobby", self.colors.WHITE)
            join_lobby_button = Button(self.screen, self.colors.ORE, 100, 200, 250, 50, "Rejoindre un lobby", self.colors.WHITE)
            self.add_button(create_lobby_button)
            self.add_button(join_lobby_button)

    def start_game_button(self):
        start_button = Button(self.screen, self.colors.WHEAT, self.screen.get_width() // 2, self.screen.get_height() // 2, 250, 50, "Lancer la partie", self.colors.WHITE)
        self.add_button(start_button)
    
    def next_turn_button(self):
        next_turn_button = Button(self.screen, self.colors.WHEAT, self.screen.get_width() // 2, self.screen.get_height() // 2, 800, 50, "Tour suivant", self.colors.WHITE)
        self.add_button(next_turn_button)

