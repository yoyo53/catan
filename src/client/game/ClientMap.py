import random
import math
import pygame
import sys

sys.path.append('..')
from lib.map.Map import Map

class ClientMap(Map):
    def __init__ (self, map, ui):
        self.map = map
        self.ui = ui
        self.radius_hex = 100

    def draw(self):
        for tile in self.map.tiles:
            self.draw_hex(tile)
            
    def draw_hex(self, tile):
        center = self.hex_to_pixel(tile, self.ui.screen)
        corners = []
        for corner in tile.corners:
            corners.append(self.corner_to_pixel(corner, self.ui.screen))
        pygame.draw.polygon(self.ui.screen, self.ui.colors.WHEAT, corners)
        pygame.draw.polygon(self.ui.screen, (0, 0, 0), corners, 1)
        #self.draw_text(self.screen, str(tile.number), center)

    #Calcul the center of the hexagon based on the coordinates
    def hex_to_pixel(self, tile, surface):
        center_x = surface.get_width() / 2 + tile.x
        center_y = surface.get_height() / 2 - tile.y
        return (center_x, center_y)

    
    def draw_text(self, surface, text, position):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, (0, 0, 0))
        rect = text_surface.get_rect(center=position)
        surface.blit(text_surface, rect)
    
    
    def corner_to_pixel(self, corner, surface):
        center_x = (surface.get_width() / 2 + corner.x) * self.radius_hex
        center_y = (surface.get_height() / 2 - corner.y) * self.radius_hex
        return (center_x, center_y)