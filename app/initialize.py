# Import the pygame module
import random

import pygame
from app.Player import Player
from app.Spell import Spell
from app.Enemy import Enemy
import time
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_z,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Init timer
clock = pygame.time.Clock()

# lets use grid 18x15, each block 64x64 px and set boundaries
SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 960

# game title
pygame.display.set_caption('Platform shooter')

# background image
background = pygame.image.load('images/background/War3.jpg')
# blocks images
dirt = pygame.image.load('images/blocks/tile.png')
lava = pygame.image.load('images/blocks/lava.png')

#player lives
lives = pygame.image.load('images/player/heart.png')

# generate font
font_score = pygame.font.SysFont('comicsans', 25)
# hp bar text
font_hp = pygame.font.SysFont('comicsans', 18)
font_enemy_hp = pygame.font.SysFont('comicsans', 12)
font_game_over = pygame.font.SysFont('comicsans', 48)
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

# enemy possible movement
movement = ['left', 'right', 'jump', 'shoot']

# collision tiles
tile_list = []

# Player first shoot
player_first_shoot = True
# Enemy first shoot
enemy_first_shoot = True

# Create player
player = Player("red")
# Player ammo
player_ammo = []

# Enemy start position (50, 600, 100, 120)

# Create enemy
enemy = Enemy(50, 600, 100, 120)
# Enemy ammo
bot_ammo = []

map_block = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    ]
# 18x15x64
tile_size = 64

def render_score_player_lives():
    # Player score
    score = font_score.render(f"Score: {player.score}", True, (255, 255, 255))
    # Player kills count
    kills = font_score.render(f"Killed: {player.kills}", True, (255, 255, 255))
    # Player hp text
    hp = font_hp.render(f"player hp: {player.hp}/100", True, (255, 255, 255))
    # enemy hp text
    enemy_hp = font_enemy_hp.render(f"{enemy.hp}/100", True, (255, 255, 255))

    if enemy.visiblity:
        screen.blit(enemy_hp, (enemy.hitbox[0]+25, enemy.hitbox[1] - 22))
    screen.blit(score, (25, 25))
    screen.blit(kills, (25, 70))
    screen.blit(hp, (950, 73))

    indent_between_lives_image = 0
    for live in range(player.lives):
        if player.lives > 1:
            screen.blit(lives, (1070 - indent_between_lives_image, 10))
            indent_between_lives_image += 50  # pixels
        else:
            screen.blit(lives, (1000, 10))

def leftrightDirection(object):
    bot = False
    invisible = False
    if not object.human:
        bot = True
        x_cord = object.x
        y_cord = object.y
        if not object.visiblity:
           invisible = True
    else:
        x_cord = object.rect.x
        y_cord = object.rect.y
    if bot and invisible:
        pass
    else:
        if object.direction_left:
            screen.blit(object.image, (x_cord, y_cord))
            object.hitbox = (x_cord + 2, y_cord, object.width - 9, object.height)
        else:
            screen.blit(object.image, (x_cord, y_cord))
            object.hitbox = (x_cord - 5, y_cord, object.width - 9, object.height)

def draw_healt_bar():
    # player health bar
    pygame.draw.rect(screen, [255, 0, 0], [930, 70, 200, 35], 1)
    pygame.draw.rect(screen, [255, 0, 0], [930, 70, 2*player.hp, 35])
    # enemy health bar
    if enemy.visiblity:
        pygame.draw.rect(screen, (255, 0, 0), (enemy.hitbox[0], enemy.hitbox[1] - 20, 100, 15))
        pygame.draw.rect(screen, (0, 128, 0), (enemy.hitbox[0], enemy.hitbox[1] - 20, 100 - (100 - enemy.hp), 15))


def drawDynamicStructures():
    # set image background
    screen.blit(background, (0, 0))
    # dynamic components health bars, lives, left right player textures
    draw_healt_bar()
    # draw collision blocks
    row_count = 0
    for row in map_block:
        col_count = 0
        for tile in row:
            if tile == 1:
                screen.blit(dirt, (col_count * tile_size, row_count * tile_size))
            if tile == 2:
                screen.blit(lava, (col_count * tile_size, row_count * tile_size))
            col_count += 1
        row_count += 1

    render_score_player_lives()
    leftrightDirection(enemy)
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
        player_ammo.append(Spell(round(object.rect.x + object.width // 2), round(object.rect.y + object.height // 2), 6, facing))
    else:
        bot_ammo.append(Spell(round(object.x + object.width // 2), round(object.y + object.height // 2), 6, facing))

# Shooting logic
def storeAmmo(ammo, object, tile_list):
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

        for tile in tile_list:
            if am.y - am.radius < tile[1][1] + tile[1][3] and am.y + am.radius > tile[1][1]:
                if am.x + am.radius > tile[1][0] and am.x - am.radius < tile[1][0] + tile[1][2]:
                    ammo.pop(ammo.index(am))
        # Bullet disapearing
        if am.x < SCREEN_WIDTH and am.x > 0:
            am.x += am.velocity * 1.5
        else:
            ammo.pop(ammo.index(am))

def createTileList():
    row_count = 0
    for row in map_block:
        col_count = 0
        for tile in row:
            if tile == 1:
                t = pygame.transform.scale(dirt, (tile_size, tile_size))
                tile_rect = t.get_rect()
                tile_rect.x = col_count * tile_size
                tile_rect.y = row_count * tile_size
                tile_obj = (t, tile_rect)
                tile_list.append(tile_obj)
            col_count += 1
        row_count += 1

createTileList()
# Main loop
while running:
    clock.tick(60)
    # print(clock.get_fps())
    game_over = False
    # if player lives 0 game over
    if player.lives <= 0:
        screen.fill((0, 0, 0))
        game_over = True
        game_over_text = font_game_over.render("Game Over", True, (255, 255, 255))
        game_over_text_score = font_game_over.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(game_over_text, (380, 60))
        screen.blit(game_over_text_score, (380, 150))
        skeleton_image = pygame.image.load('images/player/sans.png')
        screen.blit(skeleton_image, (350, 300))
        pygame.display.update()

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

    if not game_over:
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
        # if enemy.visiblity:
        #     # Enemy movement
        #     enemy_movement = random.choice(movement)
        #     if enemy_movement == 'shoot':
        #         if enemy_first_shoot:
        #             enemy_first_shoot = False
        #             bot_shooting_cooldown = time.time()
        #             shoot(enemy)
        #         # Set shooting delay for 300 ms
        #         elif time.time() - bot_shooting_cooldown >= 0.3:
        #             shoot(enemy)
        #             bot_shooting_cooldown = time.time()
        #     else:
        #         enemy.update(enemy_movement, SCREEN_WIDTH)

        # Player key handler
        if pressed_keys[K_z]:
            if player_first_shoot:
                player_first_shoot = False
                player_shooting_cooldown = time.time()
                if player.direction_left:
                    player.index = 4
                else:
                    player.index = 5
                player.image = player.player_image[player.index]
                shoot(player)
            # Set shooting delay for 300 ms
            elif time.time() - player_shooting_cooldown >= 0.5:
                if player.direction_left:
                    player.index = 4
                else:
                    player.index = 5
                player.image = player.player_image[player.index]
                shoot(player)
                player_shooting_cooldown = time.time()

        # Player shooting
        storeAmmo(player_ammo, player, tile_list)
        storeAmmo(bot_ammo, enemy, tile_list)

        # Draw dynamic components
        drawDynamicStructures()
        # check player idle status
        if True not in pressed_keys:
            player.set_idle_status()
        player.update(pressed_keys, SCREEN_WIDTH, tile_list)



