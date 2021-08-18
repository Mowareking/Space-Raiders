from data.core_funcs import *
import pygame
import math


class Bullet(pygame.sprite.Sprite):
    damage = 10
    sfx = get_sfx("laser.wav")

    def __init__(self, image, pos, angle):
        super(Bullet, self).__init__()
        self.angle = angle
        self.image = pygame.transform.rotate(image, self.angle-90)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.x = self.rect.topleft[0]
        self.y = self.rect.topleft[1]
        self.vel = 15

    def update(self):
        self.x += self.vel*math.sin(math.radians(self.angle))
        self.rect.x = self.x
        self.y -= self.vel*math.sin(math.radians(self.angle-90))
        self.rect.y = self.y

    def check_wall_collision(self) :
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            return True
        return False