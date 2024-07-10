import pygame

class Button:
    def __init__ (self, name_id : str, screen, color, margin_left, margin_top, width, height, text,text_color):
        
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
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        pygame.draw.rect(self.screen, self.color,self.button)
        button_text = self.font.render(self.text, True, self.text_color)
        self.screen.blit(button_text, (self.button.x + (self.button.width - button_text.get_width()) // 2, self.button.y + (self.button.height - button_text.get_height()) // 2))
        pygame.display.flip()

    def is_clicked(self,pos):
        return self.button.collidepoint(pos)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Button):
            return self.name_id == other.name_id
        return False