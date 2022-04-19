# Import the pygame module
import random

import pygame
from app.player import Player
from app.spell import Spell
from app.enemy import Enemy
import time
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
# player lives
lives = pygame.image.load('images/player/heart.png')

# generate font
font_score = pygame.font.SysFont('comicsans', 25)

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

# enemy possible movement
movement = ['left', 'right', 'jump', 'shoot']
# add shooting logic later
# 'shoot'

# Player first shoot
player_first_shoot = True
# Enemy first shoot
enemy_first_shoot = True

# Create player
player = Player(900, 600, 100, 113)
# Player ammo
player_ammo = []

# Enemy start position (50, 600, 100, 120)

# Create enemy
enemy = Enemy(50, 600, 100, 120)
# Enemy ammo
bot_ammo = []

def render_score_player_lives():
    # Player score
    score = font_score.render(f"score: {player.score}", True, (0, 0, 0))
    # Player kills count
    kills = font_score.render(f"killed: {player.kills}", True, (0, 0, 0))

    screen.blit(score, (25, 25))
    screen.blit(kills, (950, 70))
    indent_between_lives_image = 0
    for live in range(player.lives):
        if player.lives > 1:
            screen.blit(lives, (1000 - indent_between_lives_image, 10))
            indent_between_lives_image += 50  # pixels
        else:
            screen.blit(lives, (1000, 10))

def leftrightDirection(object):
    bot = False
    invisible = False
    if not object.human:
        bot = True
        if not object.visiblity:
           invisible = True
    if bot and invisible:
        pass
    else:
        if object.direction_left:
            screen.blit(object.image_left, (object.x, object.y))
            object.hitbox = (object.x + 2, object.y, object.width - 9, object.height)
        else:
            screen.blit(player.image_right, (object.x, object.y))
            object.hitbox = (object.x - 5, object.y, object.width - 9, object.height)

def draw_enemy_healt_bar():
    if enemy.visiblity:
        pygame.draw.rect(screen, (255, 0, 0), (enemy.hitbox[0], enemy.hitbox[1] - 20, 100, 15))
        pygame.draw.rect(screen, (0, 128, 0), (enemy.hitbox[0], enemy.hitbox[1] - 20, 100 - (100 - enemy.hp), 15))
        pygame.draw.rect(screen, [255, 0, 0], [50, 50, 300, 80], 1)
        pygame.draw.rect(screen, [255, 0, 0], [50, 50, 250, 80])
def drawWindow():
    screen.blit(background, (0, 0))
    render_score_player_lives()
    leftrightDirection(enemy)
    draw_enemy_healt_bar()
    leftrightDirection(player)
    for pa in player_ammo:
        screen.blit(pa.image_player, (pa.x, pa.y))
    for ba in bot_ammo:
        screen.blit(ba.image_enemy, (ba.x, ba.y))
    pygame.display.update()

def shoot(object):
    if object.direction_left:
        # Negative pixels stands for shooting leftside because you multiply ammo cord * facing
        facing = -1
    else:
        # Positive pixels stands for shooting rightside
        facing = 1
    # check if I am a bot
    if object.human:
        player_ammo.append(Spell(round(object.x + object.width // 2), round(object.y + object.height // 2), 6, facing))
    else:
        bot_ammo.append(Spell(round(object.x + object.width // 2), round(object.y + object.height // 2), 6, facing))

# Shooting logic
def storeAmmo(ammo, object):
    for am in ammo:
        if object.human:
            victim = enemy
        else:
            victim = player
        if am.y - am.radius < victim.hitbox[1] + victim.hitbox[3] and am.y + am.radius > victim.hitbox[1]:
            if am.x + am.radius > victim.hitbox[0] and am.x - am.radius < victim.hitbox[0] + victim.hitbox[2]:
                if not victim.human:
                    if not victim.visiblity:
                        pass
                    else:
                        victim.hit()
                        ammo.pop(ammo.index(am))
                else:
                    victim.hit()
                    ammo.pop(ammo.index(am))
        # Bullet disapearing
        if am.x < SCREEN_WIDTH and am.x > 0:
            am.x += am.velocity * 1.5
        else:
            ammo.pop(ammo.index(am))
# Main loop
while running:
    # Fps
    clock.tick(60)
    # Game delay
    pygame.time.delay(15)


    # if player lives 0 game over
    if player.lives <= 0:
        running = False

    # For loop through the event queue
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

    # kill enemy if hp goes <= 0
    if enemy.hp <= 0:
        del enemy
        player.score += 10
        player.kills += 1
        enemy = Enemy(50, 600, 100, 120)
        enemy.visiblity = False
        enemy_respawn_cooldown = time.time()

    # enemy 2 seconds respawn cooldown after being killed
    if enemy.visiblity == False:
        if time.time() - enemy_respawn_cooldown >= 2:
            enemy.visiblity = True

    # if player kills enemy, enemy is invisible for 2 seconds
    if enemy.visiblity:
        # Enemy movement
        enemy_movement = random.choice(movement)
        if enemy_movement == 'shoot':
            if enemy_first_shoot:
                enemy_first_shoot = False
                bot_shooting_cooldown = time.time()
                shoot(enemy)
            # Set shooting delay for 300 ms
            elif time.time() - bot_shooting_cooldown >= 0.3:
                shoot(enemy)
                bot_shooting_cooldown = time.time()
        else:
            enemy.update(enemy_movement, SCREEN_WIDTH)

    # Player key handler
    if pressed_keys[K_z]:
        if player_first_shoot:
            player_first_shoot = False
            player_shooting_cooldown = time.time()
            shoot(player)
        # Set shooting delay for 300 ms
        elif time.time() - player_shooting_cooldown >= 0.5:
            shoot(player)
            player_shooting_cooldown = time.time()

    # Player shooting
    storeAmmo(player_ammo, player)
    storeAmmo(bot_ammo, enemy)

    # Draw player
    player.update(pressed_keys, SCREEN_WIDTH)
    drawWindow()

