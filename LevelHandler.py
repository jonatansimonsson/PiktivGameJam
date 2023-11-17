import pygame

from Sprite import Sprite

TILE_SIZE = 20
black = (0, 0, 0)


def draw_map(level_data, screen):
    for row, line in enumerate(level_data):
        for col, char in enumerate(line):
            if char == '1':
                pygame.draw.rect(screen, black, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def load_collisions(level_data, groups):
    for row, line in enumerate(level_data):
        for col, char in enumerate(line):
            if char == '1':
                p = Sprite(black, TILE_SIZE, TILE_SIZE)
                p.rect.x = TILE_SIZE * col
                p.rect.y = TILE_SIZE * row
                p.add(groups)


class LevelHandler:
    def __init__(self):
        self.levels = []

    def load_levels(self):
        level1_path = "Levels/Level1"
        self.levels.append(level1_path)

    @staticmethod
    def load_map(path):
        with open(path, 'r') as file:
            level_data = [line.strip() for line in file]
        return level_data
