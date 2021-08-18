from data.core_funcs import *
from data.player import Player
from data.button import Button
from data.bullet import *
from data.crate import *
import data.menu as menu
import random
import pygame
import sys

PAUSE = pygame.event.Event(pygame.USEREVENT + 1)
CRATE = pygame.event.Event(pygame.USEREVENT + 2)


class Game:
    def __init__(self, win):
        self.win = win
        self.bg = get_img("game_bg.jpg")
        self.bg = pygame.transform.scale(self.bg, (1126, 500))
        self.button_sfx = get_sfx("button_click.ogg")
        self.game_over_sfx = get_sfx("explosion.wav")

    def draw_hud(self):
        border_rect = pygame.Rect(0, HEIGHT, WIDTH, HUD_HEIGHT)
        rect = pygame.Rect(5, HEIGHT + 5, WIDTH - 10, HUD_HEIGHT - 10)
        pygame.draw.rect(self.win, WHITE, border_rect)
        pygame.draw.rect(self.win, LIGHT_BLACK, rect)
        pygame.draw.line(self.win, WHITE, (WIDTH/2, HEIGHT), (WIDTH/2, HEIGHT+HUD_HEIGHT), 5)

    def run(self, red_controls, yellow_controls):
        clock = pygame.time.Clock()
        crate_timer = pygame.time.get_ticks() + random.randint(5000, 20000)
        pygame.mouse.set_visible(False)

        red = pygame.sprite.GroupSingle(Player(self.win, RED_IMG, RED_BULLET_IMG, RED_BULLET_ICON, (WIDTH/4, HEIGHT/4), 90, RED, red_controls, 1))
        yellow = pygame.sprite.GroupSingle(Player(self.win, YELLOW_IMG, YELLOW_BULLET_IMG, YELLOW_BULLET_ICON, (WIDTH*3/4, HEIGHT*3/4), 270, YELLOW, yellow_controls, 2))
        crates = pygame.sprite.Group()

        crate_imgs = {
            "LASER": pygame.transform.rotate(pygame.transform.scale(get_img("laser.png"), (20, 20)), 45),
            "MINE": pygame.transform.rotate(pygame.transform.scale(get_img("mine.png"), (20, 20)), 45)
        }

        #img = pygame.transform.rotate(pygame.transform.scale(img, (20, 20)), 45)

        run = True

        while run:
            dt = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        self.button_sfx.play()
                        run = False
                        game = menu.Menu(self.win)
                        game.run()

                    red.sprite.change_weapon(event)
                    yellow.sprite.change_weapon(event)

                    if event.key == pygame.K_r:
                        run = False
                        self.run(red_controls, yellow_controls)

                if event.type == pygame.USEREVENT + 1:
                    pygame.mouse.set_visible(True)
                    if red.sprite.health <= 0:
                        pygame.mixer.Channel(3).play(self.game_over_sfx)
                        run = False
                        self.game_over(YELLOW, "YELLOW", red_controls, yellow_controls)

                    elif yellow.sprite.health <= 0:
                        self.game_over_sfx.play()
                        run = False
                        self.game_over(RED, "RED", red_controls, yellow_controls)

                if event.type == pygame.USEREVENT + 2:
                    type = random.choice(["LASER", "LASER", "LASER", "MINE"])
                    img = crate_imgs[type]
                    crates.add(Crate(type, img))

            self.win.blit(self.bg, (0, 0))

            if red.sprite.health <= 0 or yellow.sprite.health <= 0:
                pygame.event.post(PAUSE)

            if crate_timer <= pygame.time.get_ticks():
                crate_timer = pygame.time.get_ticks() + random.randint(5000, 20000)
                pygame.event.post(CRATE)

            red.sprite.move_bullets()
            yellow.sprite.move_bullets()

            red.sprite.move_laser()
            yellow.sprite.move_laser()

            red.update(yellow, crates, dt)
            yellow.update(red, crates, dt)

            for crate in crates:
                crate.draw(self.win)
            red.draw(self.win)
            yellow.draw(self.win)
            self.draw_hud()
            red.sprite.draw_hud(20, HEIGHT + 10)
            yellow.sprite.draw_hud(WIDTH/2 + 20, HEIGHT + 10)

            pygame.display.update()

    def game_over(self, color, winner, red_controls, yellow_controls):
        restart_button = Button(self.win, WIDTH/2, 250, "RESTART", get_font(50))
        menu_button = Button(self.win, WIDTH/2, 310, "MENU", get_font(50))
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_menu = menu.Menu(self.win)
                        game_menu.run()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button.hovered_on():
                        self.button_sfx.play()
                        self.run(red_controls, yellow_controls)

                    elif menu_button.hovered_on():
                        self.button_sfx.play()
                        game_menu = menu.Menu(self.win)
                        game_menu.run()

            self.win.blit(self.bg, (0, 0))

            draw_text(self.win, f"{winner} WINS!", color, get_font(50), (WIDTH / 2, 200))
            restart_button.draw()
            menu_button.draw()
            pygame.display.update()
