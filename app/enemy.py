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


class Enemy(object):
    def __init__(self, x, y, width, height):
        super(Enemy, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        self.isJump = False
        self.human = False
        self.jumpCount = 10
        self.direction_left = False
        self.direction_right = True
        self.image_left = player_image_left
        self.image_right = player_image_right
        self.hitbox = (self.x - 5, self.y, self.width - 9, self.height)
        self.hp = 100
        self.visiblity = True

    # Delete enemy
    def __del__(self):
        pass

    # Move the sprite based on user keypresses
    def update(self, movement, SCREEN_WIDTH):
        # we will implement enemy behaviour by draw movement
        # move player and block on boundaries
        if movement == 'left' and self.x > self.velocity:
            # change bot direction if bot hits the boundary
            if self.x <= self.velocity:
                self.direction_left = False
                self.direction_right = True
            self.x -= self.velocity
            self.direction_left = True
            self.direction_right = False
        if movement == 'right' and self.x < SCREEN_WIDTH - self.width:
            self.x += self.velocity
            self.direction_left = False
            self.direction_right = True

        # jumping logic
        if not(self.isJump):
            # set jumping val to True
            if movement == 'jump':
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
