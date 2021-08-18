from data.core_funcs import *
from data.mine import *
from data.bullet import *
from data.laser import *
from data.crate import *
import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, win, img, bullet_img, bullet_icon, pos, angle, color, controls, player):
        super(Player, self).__init__()
        self.win = win
        self.color = color
        self.health = 100
        self.player = player
        self.angle = angle
        self.controls = controls
        self.original_image = img
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.fire_imgs = {
            1: get_img("fire_1.png"),
            2: get_img("fire_2.png"),
            3: get_img("fire_3.png"),
            4: get_img("fire_4.png"),
            5: get_img("fire_5.png")
        }
        self.fire_animation_count = 1
        self.fire_active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.rotate_vel = 0.2
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.vel = 0
        self.max_vel = 0.35
        self.vel_change = 0.005
        self.freeze_angle = self.angle
        self.freeze_angle_counter = True

        self.equipped = "BULLET"
        x_offset = 13 * math.sin(math.radians(self.angle))
        y_offset = 13 * math.sin(math.radians(self.angle - 90) * -1)
        self.laser = pygame.sprite.GroupSingle(Laser((self.rect.centerx+x_offset, self.rect.centery+y_offset), self.angle))
        self.bullet_img = bullet_img
        self.laser_ammo = 0
        self.bullets = pygame.sprite.Group()
        self.bullet_timer = 0
        self.mines = pygame.sprite.Group()
        self.mine_timer = 0
        self.mine_ammo = 0
        self.weapons = ["BULLET", "LASER", "MINE"]
        self.weapon_counter = 0
        self.laser_active = False
        self.bullet_icons = {
            "BULLET": bullet_icon,
            "LASER": pygame.transform.scale(get_img("laser_icon.png"), (60, 50)),
            "MINE": pygame.transform.scale(get_img("mine.png"), (60, 50))
        }

    def movement(self, delta):
        keys = pygame.key.get_pressed()
        if self.angle > 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360

        if keys[self.controls["LEFT"]]:
            self.angle += self.rotate_vel * delta
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

        if keys[self.controls["RIGHT"]]:
            self.angle -= self.rotate_vel * delta
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

        if keys[self.controls["FORWARD"]]:
            if self.vel < self.max_vel:
                self.vel += self.vel_change
            self.x += self.vel * math.sin(math.radians(self.angle)) * delta
            self.rect.centerx = self.x
            self.y += self.vel * math.sin(math.radians((self.angle - 90)*-1)) * delta
            self.rect.centery = self.y
            self.freeze_angle_counter = True
            self.fire_active = True
        else:
            if self.freeze_angle_counter:
                self.freeze_angle = self.angle
                self.freeze_angle_counter = False

            if self.vel >= self.vel_change:
                self.vel -= self.vel_change
                self.x += self.vel * math.sin(math.radians(self.freeze_angle)) * delta
                self.rect.centerx = self.x
                self.y += self.vel * math.sin(math.radians((self.freeze_angle - 90) * -1)) * delta
                self.rect.centery = self.y
            self.fire_active = False

    def change_weapon(self, event):
        if event.key == self.controls["CHANGE WEAPON"]:
            self.weapon_counter += 1
            if self.weapon_counter >= len(self.weapons):
                self.weapon_counter = 0
            self.equipped = self.weapons[self.weapon_counter]

    def shoot(self):
        keys = pygame.key.get_pressed()

        if keys[self.controls["SHOOT"]]:
            if self.equipped == "BULLET":
                if pygame.time.get_ticks() > self.bullet_timer:
                    x_offset = 13 * math.sin(math.radians(self.angle))
                    y_offset = 13 * math.sin(math.radians(self.angle-90)*-1)
                    self.bullets.add(Bullet(self.bullet_img, (self.rect.centerx+x_offset,
                                                                           self.rect.centery+y_offset), self.angle))
                    """
                    self.bullets.add(Bullet(self.bullet_img, (self.rect.centerx + x_offset,
                                                                        self.rect.centery + y_offset), self.angle - 20,
                                            ))
                    self.bullets.add(Bullet(self.bullet_img, (self.rect.centerx + x_offset,
                                                                        self.rect.centery + y_offset), self.angle + 20,
                                            ))
                    """
                    self.bullet_timer = 500 + pygame.time.get_ticks()
                    Bullet.sfx.play()

            elif self.equipped == "LASER" and self.laser_ammo > 0:
                self.laser_active = True
                self.laser_ammo -= 0.2
                self.rotate_vel = 0.05
                Laser.sfx.play()

            elif self.equipped == "MINE" and self.mine_ammo > 0:
                if pygame.time.get_ticks() > self.mine_timer:
                    self.mines.add(Mine(self.rect.center, 3000))
                    self.mine_ammo -= 1
                    self.mine_timer = pygame.time.get_ticks() + 3000
        else:
            self.rotate_vel = 0.2
            self.laser_active = False

        if self.laser_ammo <= 0:
            self.laser_active = False

    def move_bullets(self):
        self.bullets.update()
        for bullet in self.bullets:
            off_screen = bullet.check_wall_collision()
            if off_screen:
                self.bullets.remove(bullet)

    def move_laser(self):
        x_offset = 515 * math.sin(math.radians(self.angle))
        y_offset = 515 * math.sin(math.radians(self.angle - 90) * -1)
        self.laser.update(self.angle, (self.rect.centerx + x_offset, self.rect.centery + y_offset))

    def draw_bullets(self):
        self.bullets.draw(self.win)

    def draw_mines(self):
        for mine in self.mines:
            if mine.timer > pygame.time.get_ticks() or mine.in_proximity:
                mine.draw(self.win)

    def check_bullet_collision(self, enemy_bullets):
        if pygame.sprite.spritecollide(self, enemy_bullets, False):
            if pygame.sprite.spritecollide(self, enemy_bullets, True, pygame.sprite.collide_mask):
                self.health -= Bullet.damage

    def check_laser_collision(self, enemy):
        for i in range(1, 26):
            x_offset = int(40 * i * math.sin(math.radians(enemy.sprite.angle))) + enemy.sprite.rect.centerx
            y_offset = int(40 * i * math.sin(math.radians(enemy.sprite.angle - 90) * -1)) + enemy.sprite.rect.centery
            radius = 35
            if self.rect.centerx - radius <= x_offset <= self.rect.centerx + radius:
                if self.rect.centery - radius <= y_offset <= self.rect.centery + radius:
                    self.health -= Laser.damage
                    break

    def check_mine_collision(self, enemy_mines):
        for mine in enemy_mines:
            radius = 100
            if mine.rect.centerx - radius <= self.rect.centerx <= mine.rect.centerx + radius:
                if mine.rect.centery - radius <= self.rect.centery <= mine.rect.centery + radius:
                    mine.in_proximity = True
                    if mine.timer < pygame.time.get_ticks():
                        self.health -= Mine.damage
                        Mine.sfx.play()
            else:
                mine.in_proximity = False

    def check_crate_collision(self, crates):
        for crate in crates:
            if self.rect.colliderect(crate.rect):
                if crate.type == "MINE":
                    self.mine_ammo += crate.ammo
                if crate.type == "LASER":
                    self.laser_ammo += crate.ammo
                crates.remove(crate)
                Crate.sfx.play()

    def check_wall_collision(self):
        if self.rect.left > WIDTH:
            self.rect.right = 0
            self.x = self.rect.centerx

        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.x = self.rect.centerx

        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.y = self.rect.centery

        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
            self.y = self.rect.centery

    def draw_fire(self):
        fire_img = self.fire_imgs[int(self.fire_animation_count)]
        fire_img = pygame.transform.rotate(fire_img, self.angle)
        x_offset = 40 * math.sin(math.radians(self.angle))
        y_offset = 30 * math.sin(math.radians(self.angle - 90) * -1)
        fire_img_rect = fire_img.get_rect(center=(self.rect.centerx - x_offset, self.rect.centery - y_offset))
        self.win.blit(fire_img, fire_img_rect)

        self.fire_animation_count += 0.5
        if self.fire_animation_count > 5:
            self.fire_animation_count = 1

    def draw_hud(self, x, y):
        health_img_rect = HEALTH_IMG.get_rect(x=x, y=y)

        health_bar_black = pygame.rect.Rect(0, 0, 200, HEALTH_IMG.get_height() - 10)
        health_bar_red = pygame.rect.Rect(0, 0, 200*self.health/100, HEALTH_IMG.get_height() - 10)
        health_bar_black.midleft = health_img_rect.center
        health_bar_red.midleft = health_bar_black.midleft

        pygame.draw.rect(self.win, BLACK, health_bar_black)
        pygame.draw.rect(self.win, RED, health_bar_red)
        self.win.blit(HEALTH_IMG, health_img_rect)

        bullet_icon = self.bullet_icons[self.equipped]
        bullet_icon_rect = bullet_icon.get_rect(x=x, y=y+20)

        self.win.blit(bullet_icon, bullet_icon_rect)
        if self.equipped == "BULLET":
            draw_text2(self.win, "INFINITE", self.color, get_font(50), bullet_icon_rect.x + 60, bullet_icon_rect.y + 13)

        elif self.equipped == "LASER":
            draw_text2(self.win, str(int(self.laser_ammo)), BLUE, get_font(50), bullet_icon_rect.x + 60, bullet_icon_rect.y + 13)

        elif self.equipped == "MINE":
            draw_text2(self.win, str(int(self.mine_ammo)), BLACK, get_font(50), bullet_icon_rect.x + 60, bullet_icon_rect.y + 17)

    def update(self, enemy, crates, delta):
        self.movement(delta)
        self.shoot()
        self.draw_bullets()
        self.check_crate_collision(crates)
        self.check_bullet_collision(enemy.sprite.bullets)
        if enemy.sprite.laser_active:
            self.check_laser_collision(enemy)
        self.check_mine_collision(enemy.sprite.mines)
        self.check_wall_collision()
        if self.laser_active:
            self.laser.draw(self.win)
        self.draw_mines()
        if self.fire_active:
            self.draw_fire()



