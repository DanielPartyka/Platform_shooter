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
player_image_left = pygame.image.load('images/player/skeleton_idee_left.png')
player_image_right = pygame.image.load('images/player/skeleton_idee_right.png')

class Player(object):
    def __init__(self, x, y, width, height):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        self.isJump = False
        self.jumpCount = 10
        self.direction_left = True
        self.direction_right = False
        self.human = True
        self.image_left = player_image_left
        self.image_right = player_image_right
        self.hitbox = (self.x + 2, self.y, self.width - 9, self.height)
        self.lives = 3
        self.hp = 100
        self.score = 0
        self.kills = 0

    # Move the sprite based on user keypresses
    def update(self, pressed_keys, SCREEN_WIDTH, tile_list):
        dx = 0
        dy = 0

        # move player and block on left, right boundaries
        if pressed_keys[K_LEFT] and self.x > self.velocity:
            self.x -= self.velocity
            self.direction_left = True
            self.direction_right = False
        if pressed_keys[K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.velocity
            self.direction_left = False
            self.direction_right = True

        # check for collision
        for tile in tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.x + self.velocity, self.y, self.width, self.height):
                self.x += 0
            # check for collision in y direction
            if tile[1].colliderect(self.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        # jumping logic
        if not(self.isJump):
            # set jumping val to True
            if pressed_keys[K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

    def hit(self):
        self.hp -= 25
        if self.hp <= 0:
            self.lives -= 1
            self.hp = 100