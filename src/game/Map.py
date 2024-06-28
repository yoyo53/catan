import random
import math
import pygame
from Tile import Tile
from Colors import Colors
from Building import Road, Village, City


class Map:
    #attributes are hardcoded because they are the same for every game
    def __init__ (self):
        self.buildings = [] # List of buildings on the map
        self.radius_map = 2
        self.radius_hex = 100
        self.array_number = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        self.array_type = ["brick", "brick", "brick", "desert", "ore", "ore", "ore", "wood", "wood", "wood", "wood", "sheep", "sheep", "sheep", "sheep", "wheat", "wheat", "wheat", "wheat"]
        self.tiles = self.create_map()
        
    def create_map(self):
        tiles = []
        #shuffle the arrays to get random numbers and types
        random.shuffle(self.array_number)
        random.shuffle(self.array_type)
        #create the tiles in a hexagonal shape
        #hexagones have 3 coordinates x, y, z
        for x in range(-self.radius_map, self.radius_map + 1):
            for y in range(-self.radius_map, self.radius_map + 1):
                z = -x - y
                if abs(x) <= self.radius_map and abs(y) <= self.radius_map and abs(z) <= self.radius_map:
                    type = self.array_type.pop()
                    if type == "desert":
                        number = 0
                    else:
                        number = self.array_number.pop()
                    tile = Tile(type, number, x, y, z)
                    tiles.append(tile)
        return tiles
    
    def get_map(self):
        return self.tiles
    
    def print_map_attributes(self):
        for tile in self.tiles:
            print(f"Type: {tile.getType()}, Number: {tile.getNumber()}, X: {tile.getX()}, Y: {tile.getY()}, Z: {tile.getZ()}")

    def draw(self, surface):
        for tile in self.tiles:
            self.draw_hex(surface, tile)
        self.draw_buildings(surface)
        
    def draw_buildings(self, surface):
        for building in self.buildings:
            building.draw(surface)

    def draw_hex(self, surface, tile):
        center = self.hex_to_pixel(tile, surface)
        corners = self.hex_corners(center)
        colors = Colors()
        pygame.draw.polygon(surface, colors.get_color(tile.getType()), corners)
        pygame.draw.polygon(surface, (0, 0, 0), corners, 1)
        self.draw_text(surface, str(tile.getNumber()), center)

    #Calcul the center of the hexagon based on the coordinates
    def hex_to_pixel(self, tile, surface):
        x = self.radius_hex * (math.sqrt(3) * (tile.getX() + tile.getY() / 2))
        y = self.radius_hex * (3/2 * tile.getY())
        center_x = surface.get_width() / 2 + x
        center_y = surface.get_height() / 2 - y
        return (center_x, center_y)


    #Calcul the corners of the hexagon based on the center
    def hex_corners(self, center):
        corners = []
        for i in range(6):
            angle = 2 * math.pi / 6 * (i + 0.5)  # Offset angle by 0.5 for pointy-topped orientation
            x_i = center[0] + self.radius_hex * math.cos(angle)
            y_i = center[1] + self.radius_hex * math.sin(angle)
            corners.append((x_i, y_i))
        return corners

    def draw_text(self, surface, text, position):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, (0, 0, 0))
        rect = text_surface.get_rect(center=position)
        surface.blit(text_surface, rect)
    
    def get_hex_at_pixel(self, pos):
        for tile in self.tiles:
            center = self.hex_to_pixel(tile, screen)
            corners = self.hex_corners(center)
            if self.point_in_polygon(pos, corners):
                return tile
        return None

        
    def point_in_polygon(self, point, polygon):
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n+1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def get_road_position(self, pos):
        for tile in self.tiles:
            center = self.hex_to_pixel(tile, screen)
            corners = self.hex_corners(center)
            for i in range(6):
                start = corners[i]
                end = corners[(i + 1) % 6]
                if self.point_on_line(pos, start, end):
                    return Road(start, end)
        return None

    def get_village_position(self, pos):
        for tile in self.tiles:
            center = self.hex_to_pixel(tile, screen)
            corners = self.hex_corners(center)
            for corner in corners:
                if self.point_near_point(pos, corner):
                    return Village(corner)
        return None

    def get_city_position(self, pos):
        village = self.get_village_position(pos)
        if village:
            return City(village.position)
        return None

    def point_on_line(self, point, start, end):
        px, py = point
        sx, sy = start
        ex, ey = end
        distance_start = math.sqrt((px - sx) ** 2 + (py - sy) ** 2)
        distance_end = math.sqrt((px - ex) ** 2 + (py - ey) ** 2)
        line_length = math.sqrt((sx - ex) ** 2 + (sy - ey) ** 2)
        if abs((distance_start + distance_end) - line_length) < 5:  # Tolerance for clicking near the line
            return True
        return False

    def point_near_point(self, point, target, radius=10):
        px, py = point
        tx, ty = target
        distance = math.sqrt((px - tx) ** 2 + (py - ty) ** 2)
        return distance < radius

    def add_building(self, building):
      self.buildings.append(building)
    
# THIS IS FOR TEST PURPOSES ONLY
# Initialisation de Pygame
pygame.init()
WIDTH, HEIGHT = 1920, 1080
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                road_position = map.get_road_position(event.pos)
                if road_position:
                    print("add road")
                    map.add_building(road_position)
                else:
                    village_position = map.get_village_position(event.pos)
                    if village_position:
                        map.add_building(village_position)
                    else:
                        city_position = map.get_city_position(event.pos)
                        if city_position:
                            map.add_building(city_position)

    screen.fill((255, 255, 255))
    map.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()