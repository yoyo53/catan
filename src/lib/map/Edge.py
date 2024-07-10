import sys
import pygame

sys.path.append('..')

from lib.map.Corner import Corner

class Edge:
    def __init__(self, corner1, corner2):
        self.corners = [corner1, corner2] # x2
        corner1.edges.append(self)
        corner2.edges.append(self)        
        self.tiles = [] # x2 max
        self.road = None

    def __eq__(self, other):
        if isinstance(other, Edge):
            return sorted(self.corners) == sorted(other.corners)
        return False

    def __repr__(self) -> str:
        return f"**{self.corners[0]} - {self.corners[1]}**"
    
    def to_json(self):
        return {
            "corner1": self.corners[0].to_json(),
            "corner2": self.corners[1].to_json()
        }
        
    def equals_coords(self, edge2):
        return self.corners[0].x == edge2.corners[0].x and self.corners[0].y == edge2.corners[0].y and self.corners[1].x == edge2.corners[1].x and self.corners[1].y == edge2.corners[1].y
    
    staticmethod
    def from_json(json):
        corner1 = Corner.from_json(json['corner1'])
        corner2 = Corner.from_json(json['corner2'])
        return Edge(corner1, corner2)