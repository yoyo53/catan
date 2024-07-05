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
        
    def from_json(self, json):
        self.corners = [Corner(*json['corner1']), Corner(*json['corner2'])]
        return self