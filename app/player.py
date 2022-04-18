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
        self.image_left = player_image_left
        self.image_right = player_image_right

    # Move the sprite based on user keypresses
    def update(self, pressed_keys, SCREEN_WIDTH):
        # move player and block on boundaries
        if pressed_keys[K_LEFT] and self.x > self.velocity:
            self.x -= self.velocity
            self.direction_left = True
            self.direction_right = False
        if pressed_keys[K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.velocity
            self.direction_left = False
            self.direction_right = True

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