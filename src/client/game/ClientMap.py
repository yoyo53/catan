import pygame
import sys

sys.path.append('..')
from lib.map.Map import Map

class ClientMap(Map):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.radius_hex = 50
        self.margin_x = 550
        self.margin_y = 550

    def draw(self):
        for tile in self.tiles:
            self.draw_hex(tile)
            
    def draw_hex(self, tile):
        center = self.center_to_pixel(tile)
        corners = [self.corner_to_pixel(corner) for corner in tile.corners]
        pygame.draw.polygon(self.ui.screen, self.ui.colors.get_color(tile.type), corners)
        pygame.draw.polygon(self.ui.screen, (0, 0, 0), corners, 1)
        self.draw_text(str(tile.number), center)

    def center_to_pixel(self, tile):
        center_x = self.margin_x + (tile.x * self.radius_hex * 1.75)
        center_y = self.margin_y + (tile.y * self.radius_hex)
        return (center_x, center_y)

    def corner_to_pixel(self, corner):
        center_x = self.margin_x + (corner.x * self.radius_hex * 1.75)
        center_y = self.margin_y + (corner.y * self.radius_hex)
        return (center_x, center_y)

    def draw_text(self, text, position):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, (0, 0, 0))
        rect = text_surface.get_rect(center=position)
        self.ui.screen.blit(text_surface, rect)
    
    def gettile(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
        return None

    def updatetile(self, json):
        for jsontile in json["tiles"]:
            tile = self.gettile(jsontile["x"], jsontile["y"])
            tile.type = jsontile["type"]
            tile.number = jsontile["number"]