import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def move_right(self, pixels):
        self.rect.x += pixels

    def move_left(self, pixels):
        self.rect.x -= pixels

    def move_up(self, pixels):
        self.rect.y -= pixels

    def move_down(self, pixels):
        self.rect.y += pixels
