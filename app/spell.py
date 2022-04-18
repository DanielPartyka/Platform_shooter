import pygame

spell_image = pygame.image.load('images/player/fireball.png')

class Spell(object):
    def __init__(self, x, y, radius, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.velocity = 30 * facing
        self.image = spell_image