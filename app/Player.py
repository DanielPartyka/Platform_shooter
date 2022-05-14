import pygame
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

class Player():
    def __init__(self, team):
        super(Player, self).__init__()
        # status = 0 - idle right, 1 - idle left, 2 - walk right, 3 - walk left, 4 attack
        self.player_image = []
        self.index = 1
        for num in range(1, 7):
            self.player_image.append(pygame.image.load(f'images/player/player_animation/{num}.png'))
        self.image = self.player_image[self.index]
        self.rect = self.image.get_rect()
        if team == "red":
            self.rect.x = 920
        else:
            self.rect.x = 200
        self.rect.y = 450
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity = 10
        self.isJump = False
        self.team = team
        self.jumpCount = 10
        self.direction_left = False
        self.direction_right = True
        self.human = True
        self.hitbox = (self.rect.x + 2, self.rect.y, self.width - 9, self.height)
        self.lives = 5
        self.hp = 100
        self.score = 0
        self.kills = 0
        self.vel_y = 0

    # Move the sprite based on user keypresses
    def update(self, pressed_keys, SCREEN_WIDTH, tile_list):
        dx = 0
        dy = 0
        # move player and block on left, right boundaries
        if pressed_keys[K_SPACE] and self.isJump == False:
            self.vel_y = -20
            self.isJump = True
        if pressed_keys[K_SPACE] == False:
            self.isJump = False
        if pressed_keys[K_LEFT] and self.rect.x > self.velocity:
            dx -= 10
            self.direction_left = True
            self.direction_right = False
            self.index = 3
            self.image = self.player_image[self.index]
        if pressed_keys[K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.width:
            dx += 10
            self.direction_left = False
            self.direction_right = True
            self.index = 2
            self.image = self.player_image[self.index]

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision
        for tile in tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > 768:
            self.lives -= 1
            self.rect.x = 920
            self.rect.y = 450

    def set_idle_status(self):
        if self.direction_left:
            self.index = 1
        else: self.index = 0
        self.image = self.player_image[self.index]

    def hit(self):
        self.hp -= 25
        if self.hp <= 0:
            self.lives -= 1
            self.hp = 100