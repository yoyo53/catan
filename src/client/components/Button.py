import pygame

class Button:
    def __init__ (self, name_id : str, screen, color, margin_left, margin_top, width, height, text,text_color, image = None):
        
        self.name_id = name_id
        self.screen = screen
        self.color = color
        self.margin_left = margin_left - width // 2 #To center
        self.margin_top = margin_top - height // 2
        self.button = pygame.Rect(self.margin_left,self.margin_top,width,height)
        self.width = width
        self.heigth = height
        self.text = text
        self.text_color = text_color
        self.image = image
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        if self.image:
            self.screen.blit(self.image, self.button)
        else:
            pygame.draw.rect(self.screen, self.color, self.button)
            if self.text:
                text_surface = self.font.render(self.text, True, self.text_color)
                text_rect = text_surface.get_rect(center=self.button.center)
                self.screen.blit(text_surface, text_rect)
        

    def is_clicked(self,pos):
        return self.button.collidepoint(pos)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Button):
            return self.name_id == other.name_id
        return False