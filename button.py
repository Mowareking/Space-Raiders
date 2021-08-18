from .core_funcs import *
import pygame
pygame.init()


class Button:
    def __init__(self, win, x, y, text, font, width=200, height=50, border_color=WHITE, rect_color=BLACK, key=None):
        self.win = win
        self.key = key
        self.border = pygame.Rect(0, 0, width, height)
        self.rect = pygame.Rect(0, 0, width - 10, height - 10)
        self.border.center = (x, y)
        self.rect.center = self.border.center
        self.border_color = border_color
        self.rect_color = rect_color
        self.text = text
        self.text_color = border_color
        self.font = font
        self.counter = True

    def hovered_on(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.counter:
                self.border_color, self.rect_color = self.rect_color, self.border_color
                self.counter = False
            self.text_color = self.border_color
            return True
        else:
            if not self.counter:
                self.border_color, self.rect_color = self.rect_color, self.border_color
                self.counter = True
            self.text_color = self.border_color
            return False

    def update(self):
        self.hovered_on()

    def draw(self):
        self.update()
        pygame.draw.rect(self.win, self.border_color, self.border)
        pygame.draw.rect(self.win, self.rect_color, self.rect)
        draw_text(self.win, self.text, self.text_color, self.font, (self.border.centerx, self.border.centery + 5))

