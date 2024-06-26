import pygame
from components.Colors import Colors
from components.Button import Button

class UserInterface:
    def __init__(self,fps,window_width, window_height):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.colors = Colors()
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))  # Peut être défini en plein écran avec pygame.FULLSCREEN
        pygame.display.set_caption('CATAN - Multijoueur')
    
    def display_main_menu(self):
        self.screen.fill(self.colors.BLACK)
        create_lobby_button = Button(self.screen,self.colors.WHEAT,100,100,250,50,"Créer un lobby",self.colors.WHITE)
        join_lobby_button = Button(self.screen,self.colors.ORE,100,200,250,50,"Rejoindre un lobby",self.colors.WHITE)
        join_lobby_button.draw()
        create_lobby_button.draw()
        
        return create_lobby_button, join_lobby_button