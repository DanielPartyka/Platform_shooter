import pygame

spell_image_p = pygame.image.load('images/player/fireball.png')
spell_image_e = pygame.image.load('images/player/blue_fire_ball.png')

class Spell(object):
    def __init__(self, x, y, radius, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.velocity = 30 * facing
        self.image_player = spell_image_p
        self.image_enemy = spell_image_e