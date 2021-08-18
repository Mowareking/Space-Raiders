import pygame
import random
from data.core_funcs import  *


class Crate(pygame.sprite.Sprite):
    sfx = get_sfx("crate.mp3")

    def __init__(self, type, img):
        super(Crate, self).__init__()
        self.type = type
        if self.type == "MINE":
            self.ammo = 1
        if self.type == "LASER":
            self.ammo = random.randint(15, 35)
        self.image = img
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20)))
        self.border_rect = pygame.Rect(0, 0, self.rect.width + 5, self.rect.height + 5)
        self.border_rect.center = self.rect.center

    def draw(self, win):
        pygame.draw.rect(win, WHITE, self.border_rect)
        pygame.draw.rect(win, BLACK, self.rect)
        win.blit(self.image, self.rect)
