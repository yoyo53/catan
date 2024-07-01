from lib.map.Edge import Edge
from lib.map.Corner import Corner
from lib.map.Tile import Tile
from typing import List

class Map:
    #attributes are hardcoded because they are the same for every game
    def __init__ (self):
        self.tiles : List[Tile] = [] # List of tiles on the map
        self.edges : List[Edge] = [] # List of edges on the map
        self.corners : List[Corner] = [] # List of corners on the map
        
        self.buildings = [] # List of buildings on the map
        self.roads = []

        self.array_tile_number = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        self.array_tile_type = {
            "brick": 3,
            "desert": 1,
            "ore": 3,
            "wood": 4,
            "sheep": 4,
            "wheat": 4
        }
        self.create_map()

    def create_map(self):
        # For the tiles
        # x: -5 à 5
        # y: -8 à 8

        # x 2 en 2
        # y 4 en 4

        def creat_corner(tile : Tile):
            x = tile.x
            y = tile.y
            # Corner
            corner_1 = next((c for c in self.corners if c.x == x and c.y == y), Corner(x, y+2))
            corner_2 = next((c for c in self.corners if c.x == x+1 and c.y == y+1), Corner(x+1, y+1))
            corner_3 = next((c for c in self.corners if c.x == x+1 and c.y == y-1), Corner(x+1, y-1))
            corner_4 = next((c for c in self.corners if c.x == x and c.y == y-2), Corner(x, y-2))
            corner_5 = next((c for c in self.corners if c.x == x-1 and c.y == y-1), Corner(x-1, y-1))
            corner_6 = next((c for c in self.corners if c.x == x-1 and c.y == y+1), Corner(x-1, y+1))
            
            corner_list = [corner_1, corner_2, corner_3, corner_4, corner_5, corner_6]

            #Edge
            edge_1 = next((e for e in self.edges if e == Edge(corner_1, corner_2)), Edge(corner_1, corner_2))
            edge_2 = next((e for e in self.edges if e == Edge(corner_2, corner_3)), Edge(corner_2, corner_3))
            edge_3 = next((e for e in self.edges if e == Edge(corner_3, corner_4)), Edge(corner_3, corner_4))
            edge_4 = next((e for e in self.edges if e == Edge(corner_4, corner_5)), Edge(corner_4, corner_5))
            edge_5 = next((e for e in self.edges if e == Edge(corner_5, corner_6)), Edge(corner_5, corner_6))
            edge_6 = next((e for e in self.edges if e == Edge(corner_6, corner_1)), Edge(corner_6, corner_1))

            edge_list = [edge_1, edge_2, edge_3, edge_4, edge_5, edge_6]

            for corner in corner_list:
                if corner not in self.corners:
                    self.corners.append(corner)
                    
                tile.corners.append(corner)
                corner.tiles.append(tile)
                            

            for edge in edge_list:
                if edge not in self.edges:
                    self.edges.append(edge)
                    
                tile.edges.append(edge)
                edge.tiles.append(tile)   
                    
            


        void_map = [[0] * 11 for _ in range(17)]
        import numpy as np
        void_map = np.array(void_map)
        #print(void_map)
        for y in range(-6, 9, 3):
            if y % 6 == 0:
                if y % 9 == 0:
                    for x in range(-4, 6, 2):
                        tile = Tile(x, y)
                        creat_corner(tile)
                        self.tiles.append(tile)
                        #void_map[y+8][x+5] = 1
                else:
                    for x in range(-2, 4, 2):
                        #void_map[y+8][x+5] = 1
                        tile = Tile(x, y)
                        creat_corner(tile)
                        self.tiles.append(tile)
            else:
                for x in range(-3, 5, 2):
                    #void_map[y+8][x+5] = 1
                    tile = Tile(x, y)
                    creat_corner(tile)
                    self.tiles.append(tile)
        
        #print(self.edges)