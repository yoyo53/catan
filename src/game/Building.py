import pygame

class Building:
    def __init__(self, position):
        self.position = position

    def draw(self, surface):
        pass

class Road(Building):
    def __init__(self, start, end):
        super().__init__((start, end))
        self.start = start
        self.end = end

    def draw(self, surface):
        pygame.draw.line(surface, (0, 0, 255), self.start, self.end, 5)

class Village(Building):
    def __init__(self, position):
        super().__init__(position)

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), self.position, 10)

class City(Building):
    def __init__(self, position):
        super().__init__(position)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position, 15)
