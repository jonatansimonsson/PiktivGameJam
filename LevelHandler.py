import pygame
import Utils
from Sprite import Sprite

TILE_SIZE = 24
black = (0, 0, 0)
red_goal = (255, 153, 153)
blue_goal = (153, 204, 255)
gray = (128, 128, 128)
yellow = (255, 255, 0)
maroon = (128, 0, 0)


def load_collisions(level_data, walls, all_sprites, bee_goal, flower_goal, vents, keys, locked_walls, breaking_walls):
    flower_start, bee_start = [0, 0], [0, 0]
    for row, line in enumerate(level_data):
        for col, char in enumerate(line.strip()):
            if char == '0':
                pass
            elif char == '1':
                w = Sprite(black, TILE_SIZE, TILE_SIZE)
                w.rect.x = TILE_SIZE * col
                w.rect.y = TILE_SIZE * row
                w.add(walls, all_sprites)
            elif char == '2':
                g = Sprite(red_goal, TILE_SIZE, TILE_SIZE)
                g.rect.x = TILE_SIZE * col
                g.rect.y = TILE_SIZE * row
                g.add(all_sprites, bee_goal)
            elif char == '3':
                g = Sprite(blue_goal, TILE_SIZE, TILE_SIZE)
                g.rect.x = TILE_SIZE * col
                g.rect.y = TILE_SIZE * row
                g.add(all_sprites, flower_goal)
            elif char == '4':
                v = Sprite(gray, TILE_SIZE, TILE_SIZE)
                v.rect.x, v.rect.y = TILE_SIZE * col, TILE_SIZE * row
                v.add(all_sprites, vents, walls)
            elif char == '5':
                k = Sprite(yellow, TILE_SIZE, TILE_SIZE)
                k.rect.x, k.rect.y = TILE_SIZE * col, TILE_SIZE * row
                k.add(all_sprites, keys)
            elif char == '6':
                w = Sprite(yellow, TILE_SIZE, TILE_SIZE)
                w.rect.x, w.rect.y = TILE_SIZE * col, TILE_SIZE * row
                w.add(all_sprites, locked_walls, walls)
            elif char == '7':
                w = Sprite(maroon, TILE_SIZE, TILE_SIZE)
                w.rect.x, w.rect.y = TILE_SIZE * col, TILE_SIZE * row
                w.add(all_sprites, breaking_walls, walls)
            elif char == 'A':
                bee_start = [col * TILE_SIZE, row * TILE_SIZE]
            elif char == 'B':
                flower_start = [col * TILE_SIZE, row * TILE_SIZE]
    return bee_start, flower_start


class LevelHandler:
    def __init__(self):
        self.levels = []

    def load_levels(self):
        level1_path = "Levels/Level1"
        self.levels.append(level1_path)
        level2_path = "Levels/Level2"
        self.levels.append(level2_path)
        level3_path = "Levels/Level3"
        self.levels.append(level3_path)

    def level_background_path(self, level):
        return Utils.background_paths[level]

    @staticmethod
    def load_map(path):
        with open(path, 'r') as file:
            level_data = [line.strip() for line in file]
        return level_data
