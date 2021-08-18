import pygame
from data.core_funcs import *


class Mine(pygame.sprite.Sprite):
    damage = 0.2
    sfx = get_sfx("mine.mp3")

    def __init__(self, pos, timer):
        super(Mine, self).__init__()
        self.image = MINE_IMG
        self.rect = self.image.get_rect(center=pos)
        self.timer = pygame.time.get_ticks() + timer
        self.in_proximity = False

    def draw(self, win):
        win.blit(self.image, self.rect)

