import pygame
from components.Colors import Colors
from components.Button import Button
import sys

class UserInterface:
    def __init__(self, fps, window_width, window_height):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.colors = Colors()
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))  # Peut être défini en plein écran avec pygame.FULLSCREEN
        self.font = pygame.font.Font(None, 36)
        pygame.display.set_caption('CATAN - Multijoueur')
    
    def display_main_menu(self):
        self.screen.fill(self.colors.BLACK)
        create_lobby_button = Button(self.screen, self.colors.WHEAT, 100, 100, 250, 50, "Créer un lobby", self.colors.WHITE)
        join_lobby_button = Button(self.screen, self.colors.ORE, 100, 200, 250, 50, "Rejoindre un lobby", self.colors.WHITE)
        join_lobby_button.draw()
        create_lobby_button.draw()
        
        return create_lobby_button, join_lobby_button
    
    def draw_text_input_box(self, prompt, x, y, width, height):
        input_box = pygame.Rect(x, y, width, height)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((30, 30, 30))
            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            prompt_surface = self.font.render(prompt, True, self.colors.WHITE)
            self.screen.blit(prompt_surface, (x, y - 30))
            pygame.display.flip()

        self.screen.fill((0, 0, 0))
        return text

    def display_lobby(self, lobby_id, players):
        self.screen.fill(self.colors.BLACK)
        lobby_text = self.font.render(f"Lobby ID: {lobby_id}", True, self.colors.WHITE)
        self.screen.blit(lobby_text, (50, 50))
        
        y_offset = 100
        for player_number,username in players.items():
            player_text = self.font.render(f"{player_number}: {username.split('#')[0]}", True, self.colors.WHITE)
            self.screen.blit(player_text, (50, y_offset))
            y_offset += 40
        
        pygame.display.flip()
