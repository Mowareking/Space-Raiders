import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((900, 600))


def draw_text(win, text, color, font, pos):
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=pos)
    win.blit(text, text_rect)


def draw_text2(win, text, color, font, x, y):
    text = font.render(text, True, color)
    text_rect = text.get_rect(x=x, y=y)
    win.blit(text, text_rect)


def get_sfx(path):
    return pygame.mixer.Sound(os.path.join("data/assets/audio/"+path))


def get_img(path):
    return pygame.image.load(os.path.join("data/assets/graphics/"+path)).convert_alpha()


def get_font(size):
    return pygame.font.Font(os.path.join("data/assets/fonts", "Pixeltype.ttf"), size)


WIDTH, HEIGHT = 900, 500
HUD_WIDTH, HUD_HEIGHT = 900, 100
FPS = 60

YELLOW = (250, 237, 39)
RED = (255, 49, 49)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 255, 255)
LIGHT_BLACK = (64, 64, 64)

MINE_IMG = pygame.transform.scale(get_img("mine.png"), (50, 50))
HEALTH_IMG = pygame.transform.scale(get_img("health_img.png"), (30, 30))

RED_IMG = pygame.transform.scale(get_img("spaceship_red.png"), (55, 40))
RED_BULLET_IMG = get_img("red_bullet.png")
RED_BULLET_ICON = pygame.transform.scale(get_img("red_bullet_icon.png"), (60, 50))

YELLOW_IMG = pygame.transform.scale(get_img("spaceship_yellow.png"), (55, 40))
YELLOW_BULLET_IMG = get_img("yellow_bullet.png")
YELLOW_BULLET_ICON = pygame.transform.scale(get_img("yellow_bullet_icon.png"), (60, 50))
