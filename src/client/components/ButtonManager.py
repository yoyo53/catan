from components.Button import Button
import os
import pygame

assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..','..','assets')



class ButtonManager:
    def __init__(self, screen, colors):
        self.buttons = []
        self.screen = screen
        self.colors = colors

    def add_button_if_not_exist(self, button):# Only create buttons if there are none, ON CREEE PAS DES BOUTONS A CHAQUE FRAME HEIN LUCAS
        for b in self.buttons:
            if b == button:
                return
        self.buttons.append(button)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()

    def clear_buttons(self):
        self.buttons = []

    def create_main_menu_buttons(self):
        create_lobby_button = Button("create_lobby",self.screen, self.colors.WHEAT, 100, 100, 250, 50, "Créer un lobby", self.colors.WHITE)
        join_lobby_button = Button("join_lobby",self.screen, self.colors.ORE, 100, 200, 250, 50, "Rejoindre un lobby", self.colors.WHITE)
        self.add_button_if_not_exist(create_lobby_button)
        self.add_button_if_not_exist(join_lobby_button)

    def start_game_button(self):
        start_button = Button("start_game", self.screen, self.colors.WHEAT, self.screen.get_width() // 2, self.screen.get_height() // 2, 250, 50, "Lancer la partie", self.colors.WHITE)
        self.add_button_if_not_exist(start_button)
    
    def next_turn_button(self):
        NEXT_TURN_IMG = pygame.image.load(os.path.join(assets_path, 'next_turn.png')).convert_alpha()
        next_turn_button = Button("next_turn", self.screen, self.colors.WHEAT, 1190,600, 50, 50, "Tour suivant", self.colors.WHITE, image=NEXT_TURN_IMG)
        self.add_button_if_not_exist(next_turn_button)

    def create_road_button(self):
        ROAD_IMG = pygame.image.load(os.path.join(assets_path, 'road.png')).convert_alpha()
        road_button = Button("create_road", self.screen, self.colors.RED, 890, 600, 50, 50, "Construire une route", self.colors.WHITE, image=ROAD_IMG)
        self.add_button_if_not_exist(road_button)

    def create_settlement_button(self):
        HOUSE_IMG = pygame.image.load(os.path.join(assets_path, 'house.png')).convert_alpha()
        settlement_button = Button("create_settlement", self.screen, self.colors.GREEN, 990, 600, 50, 50, "Construire un village", self.colors.WHITE, image=HOUSE_IMG)
        self.add_button_if_not_exist(settlement_button)
    
    def upgrade_settlement_button(self):
        VILLAGE_IMG = pygame.image.load(os.path.join(assets_path, 'village.png')).convert_alpha()
        upgrade_button = Button("upgrade_settlement", self.screen, self.colors.BLUE, 1090, 600, 50, 50, "Améliorer un village", self.colors.WHITE, image=VILLAGE_IMG)
        self.add_button_if_not_exist(upgrade_button)