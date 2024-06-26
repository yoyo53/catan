import random
import math
import pygame
from Tile import Tile

class Map:
    #attributes are hardcoded because they are the same for every game
    def __init__ (self):
        self.radius = 2
        self.arrayNumber = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        self.arrayType = ["brick", "brick", "brick", "desert", "ore", "ore", "ore", "wood", "wood", "wood", "wood", "sheep", "sheep", "sheep", "sheep", "wheat", "wheat", "wheat", "wheat"]
        self.tiles = self.createMap()
        
    def createMap(self):
        tiles = []
        #shuffle the arrays to get random numbers and types
        random.shuffle(self.arrayNumber)
        random.shuffle(self.arrayType)
        #create the tiles in a hexagonal shape
        #hexagones have 3 coordinates x, y, z
        for x in range(-self.radius, self.radius + 1):
            for y in range(-self.radius, self.radius + 1):
                z = -x - y
                if abs(x) <= self.radius and abs(y) <= self.radius and abs(z) <= self.radius:
                    type = self.arrayType.pop()
                    if type == "desert":
                        number = 0
                    else:
                        number = self.arrayNumber.pop()
                    tile = Tile(type, number, x, y, z)
                    tiles.append(tile)
        return tiles
    
    def getMap(self):
        return self.tiles
    
    def printMapAttributes(self):
        for tile in self.tiles:
            print(f"Type: {tile.getType()}, Number: {tile.getNumber()}, X: {tile.getX()}, Y: {tile.getY()}, Z: {tile.getZ()}")

    def draw(self, surface):
        for tile in self.tiles:
            self.draw_hex(surface, tile)

    def draw_hex(self, surface, tile):
        center = self.hex_to_pixel(tile)
        corners = self.hex_corners(center)
        pygame.draw.polygon(surface, self.get_color(tile.getType()), corners)
        pygame.draw.polygon(surface, (0, 0, 0), corners, 1)
        self.draw_text(surface, str(tile.getNumber()), center)

    def hex_to_pixel(self, tile):
        RADIUS = 50
        x = RADIUS * (3/2 * tile.getX())
        y = RADIUS * (math.sqrt(3) * (tile.getY() + tile.getX() / 2))
        return (400 + x, 300 - y)

    def hex_corners(self, center):
        RADIUS = 50
        corners = []
        for i in range(6):
            angle = 2 * math.pi / 6 * i
            x_i = center[0] + RADIUS * math.cos(angle)
            y_i = center[1] + RADIUS * math.sin(angle)
            corners.append((x_i, y_i))
        return corners

    def get_color(self, tile_type):
        colors = {
            'brick': (139, 69, 19),
            'desert': (210, 180, 140),
            'ore': (169, 169, 169),
            'wood': (34, 139, 34),
            'sheep': (50, 205, 50),
            'wheat': (255, 223, 0),
            'water': (0, 191, 255)
        }
        return colors.get(tile_type, (255, 255, 255))

    def draw_text(self, surface, text, position):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, (0, 0, 0))
        rect = text_surface.get_rect(center=position)
        surface.blit(text_surface, rect)
      
# THIS IS FOR TEST PURPOSES ONLY  
# Initialisation de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carte Hexagonale de Catan")
clock = pygame.time.Clock()

# Création de la carte
map = Map()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    map.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()