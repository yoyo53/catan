from components.UserInterface import UserInterface
from components.User import User
import pygame
import sys

if __name__ == "__main__":

    UI = UserInterface(60, 1280, 720)
    username = UI.draw_text_input_box("Pseudo", 50, 50, 50, 50) 
    user = User(username, UI)
    
    create_lobby_button, join_lobby_button = UI.display_main_menu()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if create_lobby_button.is_clicked(event.pos):
                    user.create_lobby()
                elif join_lobby_button.is_clicked(event.pos):
                    lobby_id = UI.draw_text_input_box("ID du lobby", 50,50,50,50)
                    user.join_lobby(lobby_id)

        user.handle_messages()

        pygame.display.update()
        UI.clock.tick(UI.fps)

    pygame.quit()
    sys.exit()
