
from components.UserInterface import UserInterface
from components.User import User
import pygame
import sys


if __name__ == "__main__":

    UI = UserInterface(60, 1280, 720)
    username = UI.draw_text_input_box("Pseudo", 50 , 50, 50 , 50) 
    user = User(username)
    
    create_lobby_button, join_lobby_button = UI.display_main_menu()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if create_lobby_button.is_clicked(event.pos):
                    print("create lobby")
                    user.create_lobby()
                    #join room
                    #start game

                elif join_lobby_button.is_clicked(event.pos):
                    print("join lobby")

        pygame.display.update()
        UI.clock.tick(UI.fps)


    pygame.quit()
    sys.exit()
    

