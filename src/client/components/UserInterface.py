import pygame
from components.Colors import Colors
import sys
from game.ClientMap import ClientMap

sys.path.append('..')
from components.ButtonManager import ButtonManager
from components.Button import Button


class UserInterface:
    def __init__(self, fps, window_width, window_height):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.colors = Colors()
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.buttonmanager = ButtonManager(self.screen, self.colors)
        pygame.display.set_caption('CATAN - Multijoueur')
        self.status = "main_menu"
        self.user = None
        self.error = None
        self.buttons = []


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

    def display_error(self, error_message):
        error_popup_width = 400
        error_popup_height = 200
        error_popup_rect = pygame.Rect(
            (self.WINDOW_WIDTH - error_popup_width) // 2,
            (self.WINDOW_HEIGHT - error_popup_height) // 2,
            error_popup_width,
            error_popup_height - 50
        )

        close_button = Button("close_button", self.screen, self.colors.RED,
                              (self.WINDOW_WIDTH // 2) - 50,
                              (self.WINDOW_HEIGHT // 2) + 10,
                              100, 40,
                              "Close", self.colors.WHITE)

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if close_button.is_clicked(event.pos):
                        done = True
                        self.error = None

            pygame.draw.rect(self.screen, self.colors.WHEAT, error_popup_rect)

            error_text_surface = self.font.render(error_message, True, self.colors.BLACK)
            error_text_rect = error_text_surface.get_rect(center=error_popup_rect.center)
            self.screen.blit(error_text_surface, error_text_rect)

            close_button.draw()

            pygame.display.flip()

        self.screen.fill(self.colors.BLACK)

    def display_lobby(self, lobby):
        lobby_id = lobby.lobby_id
        players = lobby.players
        lobby_text = self.font.render(f"Lobby ID: {lobby_id}", True, self.colors.WHITE)
        self.screen.blit(lobby_text, (50, 50))

        y_offset = 100
        for player_number, username in players.items():
            player_text = self.font.render(f"{player_number}: {username.split('#')[0]}", True, self.colors.WHITE)
            self.screen.blit(player_text, (50, y_offset))
            y_offset += 40


    def handle_events(self, event):
        for button in self.buttonmanager.buttons:
            if button.is_clicked(event.pos):
                return button
        return None
    def wait_for_click(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return event.pos
    def draw_hud(self, game):
        self.screen.fill(self.colors.BLACK)
        game.map.draw()
        road_button = Button("create_road", self.screen, self.colors.RED, 500, 500, 50, 50, "Construire une route", self.colors.WHITE)
        road_button.draw()
        self.buttons.append(road_button)

    def draw_map(self, map):
        clientMap = ClientMap(map, self)
        clientMap.draw()

    def draw_game(self, game):
        game.map.draw()

    def display_turn_order(self, turn_order):
        y_offset = 50
        for player in turn_order:
            player_name = player[0]
            order = player[1]
            turn_order_text = self.font.render(f"{player_name} - {order}", True, self.colors.WHITE)
            text_width = turn_order_text.get_width()
            x = self.WINDOW_WIDTH - text_width - 50
            y = y_offset
            self.screen.blit(turn_order_text, (x, y))
            y_offset += 50

    def display_end_turn_button(self):
        end_turn_button = Button("end_turn", self.screen, self.colors.ORE, self.WINDOW_WIDTH - 250, self.WINDOW_HEIGHT - 100, 250, 50, "Terminer le tour", self.colors.WHITE)
        end_turn_button.draw()
        self.buttons.append(end_turn_button)
    def draw(self):
        self.screen.fill(self.colors.BLACK)
        self.buttonmanager.clear_buttons()
        match self.status:
            case "main_menu":
                self.buttonmanager.create_main_menu_buttons()
            case "lobby":
                self.display_lobby(self.user.lobby)
                if(self.user.lobby.lobby_id in self.user.hosted_games):
                    self.buttonmanager.start_game_button()
            case "game_started":
                self.draw_game(self.user.game)
                self.display_turn_order(self.user.game.turn_order)
                if self.user.game.is_player_turn(self.user.my_turn):
                    self.buttonmanager.next_turn_button()
                    self.buttonmanager.create_road_button()
                    self.buttonmanager.create_settlement_button()
                    self.buttonmanager.upgrade_settlement_button()
            case _:
                print("Unknown status")
                print(self.status)
        if self.error:
            self.display_error(self.error)
        

            

        self.buttonmanager.draw_buttons()

    def change_state(self, state):
        self.status = state
        self.buttonmanager.clear_buttons()
