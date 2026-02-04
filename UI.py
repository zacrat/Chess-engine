import pygame
from tkinter import filedialog

class TextBox():
    def __init__(self, x,y,width,height,title,colour , font, border_colour = (0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.colour = colour
        self.font = font
        self.border_colour = border_colour
        self.rect = pygame.Rect(x, y, width, height)
        self.border = pygame.Rect(x-4, y-4, width+8, height+8)
        self.header = font.render(self.title, True, (0, 0, 0))
    def draw(self, screen, content):
        pygame.draw.rect(screen, self.colour, self.rect)
        pygame.draw.rect(screen, self.border_colour, self.border, 4)
        screen.blit(self.header, (self.x-20, self.y-60))
        data = self.font.render(content, True, (0,0,0))
        screen.blit(data, (self.x, self.y))

class button:
    def __init__(self,function, x, y, width, height, text='', colour_idle=(255, 255, 255), colour_hover=(200, 200, 200), font_size=30):
        self.function = function
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour_idle = colour_idle
        self.colour_hover = colour_hover
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            colour = self.colour_hover
        else:
            colour = self.colour_idle
        pygame.draw.rect(screen, colour, self.rect, border_radius=5)
        if self.text:
            text_surf = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                return True
        return False



def choose_file():
    file_path = filedialog.askopenfilename()
    return file_path