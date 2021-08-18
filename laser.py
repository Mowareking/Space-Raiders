from data.core_funcs import *
import pygame


class Laser(pygame.sprite.Sprite):
    damage = 0.6
    sfx = get_sfx("laser.mp3")

    def __init__(self, pos, angle):
        super(Laser, self).__init__()
        self.angle = angle
        self.original_image = pygame.transform.scale(get_img("laser.png"), (1030, 20))
        self.image = pygame.transform.rotate(self.original_image, self.angle-90)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)

    def update(self, angle, pos):
        self.image = pygame.transform.rotate(self.original_image, angle-90)
        self.rect = self.image.get_rect(center=pos)
