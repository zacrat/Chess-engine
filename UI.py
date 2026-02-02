import pygame
from tkinter import filedialog

class button:
    def __init__(self,function, x, y, width, height, text='', color_idle=(255, 255, 255), color_hover=(200, 200, 200), font_size=30):
        self.function = function
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.color_hover
        else:
            color = self.color_idle
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
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