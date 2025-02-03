import pygame

class Button:
    def __init__(self, Surface, width, height, text='', font=None, font_size=10, pos=(0, 0), color=(196, 196, 194), text_color=(0,0,0)):
        self.Surface = Surface
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size   
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.text_color = text_color

        if font:
            self.font = font
        else:
            self.font = pygame.font.SysFont('timesnewroman', self.font_size)

        self.clicked = False

    def draw(self):
        action = False

        pygame.draw.rect(self.Surface, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            self.Surface.blit(text_surface, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action