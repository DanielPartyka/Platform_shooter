# Import the pygame module
import pygame

from app.player import Player
from app.spell import Spell
import pygame
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_z,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Initialize pygame
pygame.init()

# Init timer
clock = pygame.time.Clock()

# Define constants for the screen width and height
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# background image
background = pygame.image.load('images/background/War3.png')

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

# create player
player = Player(50, 600, 100, 80)
ammo = []

def drawWindow():
    screen.blit(background, (0, 0))
    if player.direction_left:
        screen.blit(player.image_left, (player.x, player.y))
    else:
        screen.blit(player.image_right, (player.x, player.y))
    for am in ammo:
        screen.blit(am.image, (am.x, am.y))
    pygame.display.update()

# Main loop
while running:
    # Fps
    clock.tick(60)
    # delay
    pygame.time.delay(15)
    # for loop through the event queue
    for event in pygame.event.get():
        pressed_keys = pygame.key.get_pressed()
        # Check for z KEYDOWN event
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    if pressed_keys[K_z]:
        if player.direction_left:
            facing = -1
        else:
            facing = 1
        ammo.append(Spell(round(player.x + player.width // 2), round(player.y + player.height // 2), 6, facing))
    # Shooting logic
    for am in ammo:
        if am.x < SCREEN_WIDTH and am.x > 0:
            am.x += am.velocity
        else:
            ammo.pop(ammo.index(am))

    # Draw player
    player.update(pressed_keys, SCREEN_WIDTH)
    drawWindow()

