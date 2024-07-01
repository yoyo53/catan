import pygame
import sys
from components.UserInterface import UserInterface
from components.User import User

from lib.Building import Building

if __name__ == "__main__":

    UI = UserInterface(60, 1920, 1080)
    
    #username = UI.draw_text_input_box("Pseudo", 50, 50, 50, 50) 
    #user = User(username, UI)
    
    #UI.display_main_menu()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            """elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_button = UI.handle_events(event)
                if clicked_button:
                    if clicked_button.text == "Créer un lobby":
                        user.create_lobby()
                    elif clicked_button.text == "Rejoindre un lobby":
                        lobby_id = UI.draw_text_input_box("ID du lobby", 50, 50, 50, 50)
                        user.join_lobby(lobby_id)
                    elif clicked_button.text == "Lancer la partie":
                        user.start_game()"""

        #user.handle_messages()

        UI.draw_map()
        pygame.display.flip()

        pygame.display.update()
        UI.clock.tick(UI.fps)

    pygame.quit()
    sys.exit()
