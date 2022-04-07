import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(pos)
        )
    def fire(self):
        self.rect.move_ip(-20, 0)
        if self.rect.left < 0:
            self.kill()