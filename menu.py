import data.game as game
from data.core_funcs import *
from data.button import Button
import pygame
import sys
pygame.init()
pygame.mixer.init()


class Menu:
    red_controls = {
        "FORWARD": pygame.K_w,
        "LEFT": pygame.K_a,
        "RIGHT": pygame.K_d,
        "SHOOT": pygame.K_f,
        "CHANGE WEAPON": pygame.K_g
    }
    yellow_controls = {
        "FORWARD": pygame.K_UP,
        "LEFT": pygame.K_LEFT,
        "RIGHT": pygame.K_RIGHT,
        "SHOOT": pygame.K_COMMA,
        "CHANGE WEAPON": pygame.K_PERIOD
    }

    def __init__(self, win):
        self.win = win
        self.bg = get_img("space.png")
        self.bg = pygame.transform.scale(self.bg, (1000, 600))
        self.sfx = get_sfx("button_click.ogg")

    def choose_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    return event.key

    def keybinds(self):
        red_buttons = []
        yellow_buttons = []
        for count, key in enumerate(self.red_controls.keys()):
            red_buttons.append(Button(self.win, WIDTH/2 - 80, 150 + count * 60, pygame.key.name(self.red_controls[key]).upper(), get_font(50), key=key))

        for count, key in enumerate(self.yellow_controls.keys()):
            yellow_buttons.append(Button(self.win, WIDTH*3/4, 150 + count * 60, pygame.key.name(self.yellow_controls[key]).upper(), get_font(50), key=key))

        back_button = Button(self.win, WIDTH/2 - 10, 500, "BACK", get_font(50))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    self.run()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.hovered_on():
                        self.sfx.play()
                        run = False
                        self.run()

                    for button in red_buttons:
                        if button.hovered_on():
                            key = self.choose_key()
                            if (key not in self.yellow_controls.values()) and (key not in self.red_controls.values()):
                                self.red_controls[button.key] = key
                                button.text = pygame.key.name(key).upper()

                    for button in yellow_buttons:
                        if button.hovered_on():
                            key = self.choose_key()
                            if key not in self.red_controls.values() and (key not in self.yellow_controls.values()):
                                self.yellow_controls[button.key] = key
                                button.text = pygame.key.name(key).upper()

            self.win.blit(self.bg, (-100, 0))

            draw_text(self.win, "RED", RED, get_font(80), (WIDTH/2 - 80, 50))
            draw_text(self.win, "YELLOW", YELLOW, get_font(80), (WIDTH*3/4, 50))
            draw_text(self.win, "Made by Jahin Rahman", WHITE, get_font(40), (WIDTH - 150, HEIGHT+HUD_HEIGHT-20))

            draw_text2(self.win, "FORWARD", WHITE, get_font(60), 30, 135)
            draw_text2(self.win, "TURN LEFT", WHITE, get_font(50), 30, 195)
            draw_text2(self.win, "TURN RIGHT", WHITE, get_font(50), 30, 255)
            draw_text2(self.win, "SHOOT", WHITE, get_font(50), 30, 315)
            draw_text2(self.win, "CHANGE WEAPON", WHITE, get_font(50), 30, 375)

            draw_text2(self.win, "ESC - BACK TO MENU", WHITE, get_font(40), 30, 450)
            draw_text2(self.win, "R - RESTART", WHITE, get_font(40), 30, 485)

            for button in red_buttons:
                button.draw()

            for button in yellow_buttons:
                button.draw()

            back_button.draw()

            pygame.display.update()

    def run(self):
        start_button = Button(self.win, WIDTH / 2, (HEIGHT+HUD_HEIGHT) / 2 - 40, "START", get_font(50))
        keybinds_button = Button(self.win, WIDTH / 2, (HEIGHT+HUD_HEIGHT) / 2 + 40, "KEYBINDS", get_font(50))
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.hovered_on():
                        self.sfx.play()
                        games = game.Game(self.win)
                        games.run(self.red_controls, self.yellow_controls)

                    if keybinds_button.hovered_on():
                        self.sfx.play()
                        self.keybinds()

            self.win.blit(self.bg, (-100, 0))
            draw_text(self.win, "SPACE", YELLOW, get_font(100), (WIDTH / 2 - 120, 100))
            draw_text(self.win, "RAIDERS", RED, get_font(100), (WIDTH / 2 + 120, 100))

            start_button.draw()
            keybinds_button.draw()

            pygame.display.update()

