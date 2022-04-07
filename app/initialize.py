# Import the pygame module
import pygame

from app.bullet import Bullet
from app.player import Player
from app.enemy import Enemy
import pygame
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_z,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

# create player
player = Player()

# create enemy
enemy = Enemy()

# players and eniemies group
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
# all_sprites.add(bullet)

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for z KEYDOWN event
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_z]:
        bullet = Bullet((player.rect.left, player.rect.top))
        bullets.add(bullet)

    # Update the player sprite based on user keypresses
    # if bullets.empty():
    #     print('eloo')
    # else:
    #     bullet.fire()


    player.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    for entity in bullets:
        screen.blit(entity.surf, entity.rect)
    # # Draw the player on the screen
    # screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()
