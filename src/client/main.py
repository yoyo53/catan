from WebsocketClient import WebsocketClient
from threading import Thread
from components.UserInterface import UserInterface
import pygame
import sys
import asyncio
import time
import json


SERVER_URL = "ws://127.0.0.1:8765"


if __name__ == "__main__":
    client = WebsocketClient(SERVER_URL)
    Thread(target=client.start).start()
    time.sleep(1)

    UI = UserInterface(60, 1280, 720) 
    create_lobby_button, join_lobby_button = UI.display_main_menu()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if create_lobby_button.is_clicked(event.pos):
                    print("creer lobby")
                    #join room
                    #start game

                elif join_lobby_button.is_clicked(event.pos):
                    print("join lobby")

        pygame.display.update()
        UI.clock.tick(UI.fps)


    pygame.quit()
    sys.exit()

