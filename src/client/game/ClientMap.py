import math
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
        self.draw_roads()
        self.draw_buldings()
            
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

    def get_edge_from_click(self, pos):
        for edge in self.edges:
            start_corner = edge.corners[0]
            end_corner = edge.corners[1]
            start_pixel = self.corner_to_pixel(start_corner)#, self.ui.screen)
            end_pixel = self.corner_to_pixel(end_corner)#, self.ui.screen)
            center_x = (start_pixel[0] + end_pixel[0]) / 2
            center_y = (start_pixel[1] + end_pixel[1]) / 2
            radius = 40 #((end_pixel[0] - start_pixel[0]) + (end_pixel[1] - start_pixel[1])) / 2
            hit_box = pygame.Rect(center_x - radius, center_y - radius, 2 * radius, 2 * radius)
            #pygame.draw.circle(self.ui.screen, (0, 0, 0), (int(center_x), int(center_y)), int(radius), 1)
            if hit_box.collidepoint(pos):
                return edge
        return None
    
    def get_corner_from_click(self, pos):
        for corner in self.corners:
            corner_pixel = self.corner_to_pixel(corner)#, self.ui.screen)
            hit_box = pygame.Rect(corner_pixel[0] - 20, corner_pixel[1] - 20, 40, 40)
            #pygame.draw.circle(self.ui.screen, (0, 0, 0), corner_pixel, 10, 1)
            if hit_box.collidepoint(pos):
                return corner
            
        return None
    
    def draw_roads(self):
        #print("Roads ?")
        for road in self.roads:
            #print("Road", road)
            start_corner = road.edge.corners[0]
            end_corner = road.edge.corners[1]
            start_pixel = self.corner_to_pixel(start_corner)
            end_pixel = self.corner_to_pixel(end_corner)
            pygame.draw.line(self.ui.screen, road.owner.color, start_pixel, end_pixel, 10)

    def draw_buldings(self):
        for building in self.buildings:
            center = self.corner_to_pixel(building.corner)
            if building.type == "settlement":
                pygame.draw.circle(self.ui.screen, building.owner.color, center, 17)
            elif building.type == "city":
                pygame.draw.polygon(self.ui.screen, building.owner.color, self.get_hexagon_points(center, 25))

    def get_hexagon_points(self, center, radius):
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.pi / 180 * angle_deg
            x = center[0] + radius * math.cos(angle_rad)
            y = center[1] + radius * math.sin(angle_rad)
            points.append((x, y))
        return points