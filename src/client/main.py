import pygame
import sys
from components.UserInterface import UserInterface
from components.User import User

from lib.map.Map import Map

if __name__ == "__main__":

    UI = UserInterface(60, 1280, 720)
    username = UI.draw_text_input_box("Pseudo", 50, 50, 50, 50) 
    user = User(username, UI)
    
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_button = UI.handle_events(event)
                if clicked_button:
                    if clicked_button.name_id == "create_lobby":
                        user.create_lobby()
                    elif clicked_button.name_id == "join_lobby":
                        lobby_id = UI.draw_text_input_box("ID du lobby", 50, 50, 50, 50)
                        user.join_lobby(lobby_id)
                    elif clicked_button.name_id == "start_game":
                        user.start_game()
                        user.get_turn_order()
                    elif clicked_button.name_id == "create_road":
                        mouse_click = UI.wait_for_click()
                        edge = user.game.map.get_edge_from_click(mouse_click)
                        print("Edge clicked", edge)
                        if edge:
                            user.build_road(edge)
                        #UI.draw_hud(user.game)
                    elif clicked_button.name_id == "create_settlement":
                        mouse_click = UI.wait_for_click()
                        corner = user.game.map.get_corner_from_click(mouse_click)
                        print("Corner clicked", corner)
                        if corner:
                            user.build_settlement(corner)

                    elif clicked_button.name_id == "upgrade_settlement":
                        mouse_click = UI.wait_for_click()
                        corner = user.game.map.get_corner_from_click(mouse_click)
                        print("Corner clicked", corner)
                        if corner:
                            user.upgrade_settlement(corner)
                            

                    

        user.handle_messages()
        UI.draw()

        pygame.display.update()
        UI.clock.tick(UI.fps)

    pygame.quit()
    sys.exit()