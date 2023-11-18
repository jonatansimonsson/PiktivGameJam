import pygame
import sys

from pygame.sprite import spritecollide, collide_rect, groupcollide

from LevelHandler import LevelHandler, load_collisions
from Sprite import Sprite
from Player import Player

# Initialize Pygame
pygame.init()

# Set up display
width, height = 960, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Cubes")
font = pygame.font.SysFont("Comic Sans", 100)


# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
text_color = (255, 0, 255)

tile_size = 24
cube_speed = 6

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
bee_goal = pygame.sprite.Group()
flower_goal = pygame.sprite.Group()
vents = pygame.sprite.Group()
keys_group = pygame.sprite.Group()
locked_walls = pygame.sprite.Group()
players = pygame.sprite.Group()
breaking_walls = pygame.sprite.Group()

# Load level info and collisions
level_handler = LevelHandler()
level_handler.load_levels()
level_data = level_handler.load_map(level_handler.levels[0])
bee_spawn, flower_spawn = load_collisions(level_data, walls, all_sprites, bee_goal, flower_goal, vents, keys_group, locked_walls, breaking_walls)
current_level = 0
background_surface = pygame.image.load(level_handler.level_background_path(current_level))
background_rect = background_surface.get_rect(topleft=(0, 0))
screen.blit(background_surface, background_rect)

# Create players
player1 = Player(red, tile_size, tile_size, bee_spawn)
player2 = Player(blue, tile_size, tile_size, flower_spawn)
player1.add(all_sprites, players)
player2.add(all_sprites, players)


def check_level_complete():
    if not player1.rect.collidelist(bee_goal.sprites()) and not player2.rect.collidelist(flower_goal.sprites()):
        return True
    else:
        return False


def go_next_level(current):
    current += 1
    # Set background based on level
    bg_surface = pygame.image.load(level_handler.level_background_path(current))
    bg_rect = background_surface.get_rect(topleft=(0, 0))
    if len(level_handler.levels) >= current:
        reload_sprites()
        level_data = level_handler.load_map(level_handler.levels[current-1])
        bee_spawn, flower_spawn = load_collisions(level_data, walls, all_sprites, bee_goal, flower_goal, vents, keys_group, locked_walls, breaking_walls)
        player1 = Player(red, tile_size, tile_size, bee_spawn)
        player2 = Player(blue, tile_size, tile_size, flower_spawn)
        player1.add(all_sprites, players)
        player2.add(all_sprites, players)
        return current, level_data, player1, player2, bg_surface, bg_rect
    else:
        pass


def reload_sprites():
    for sprite in all_sprites:
        sprite.kill()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    if current_level:
        # Update cube positions based on key presses
        if keys[pygame.K_LEFT]:
            player1.rect.x -= cube_speed
            player2.rect.x -= cube_speed
            for wall in walls:
                if collide_rect(player2, wall):
                    player2.rect.left = wall.rect.right
                if collide_rect(player1, wall):
                    player1.rect.left = wall.rect.right

                for w in breaking_walls:
                    if collide_rect(player2, w):
                        w.kill()

            if collide_rect(player1, player2):
                if player1.rect.x > player2.rect.x:
                    player1.rect.left = player2.rect.right
                else:
                    player2.rect.left = player1.rect.right

        if keys[pygame.K_RIGHT]:
            player1.rect.x += cube_speed
            player2.rect.x += cube_speed
            for wall in walls:
                if collide_rect(player2, wall):
                    player2.rect.right = wall.rect.left
                if collide_rect(player1, wall):
                    player1.rect.right = wall.rect.left

                for w in breaking_walls:
                    if collide_rect(player2, w):
                        w.kill()

            if collide_rect(player1, player2):
                if player1.rect.x < player2.rect.x:
                    player1.rect.right = player2.rect.left
                else:
                    player2.rect.right = player1.rect.left

        if keys[pygame.K_UP]:
            player1.rect.y -= cube_speed
            player2.rect.y -= cube_speed
            for wall in walls:
                if collide_rect(player2, wall):
                    player2.rect.top = wall.rect.bottom
                if collide_rect(player1, wall):
                    player1.rect.top = wall.rect.bottom

                    for w in breaking_walls:
                        if collide_rect(player2, w):
                            w.kill()

                if len(vents) > 1:
                    if collide_rect(player1, vents.sprites()[0]):
                        player1.rect.bottom = vents.sprites()[1].rect.top
                        player1.rect.right = vents.sprites()[1].rect.right
                    elif collide_rect(player1, vents.sprites()[1]):
                        player1.rect.top = vents.sprites()[0].rect.bottom
                        player1.rect.right = vents.sprites()[0].rect.right

            if collide_rect(player1, player2):
                if player1.rect.y > player2.rect.y:
                    player1.rect.top = player2.rect.bottom
                else:
                    player2.rect.top = player1.rect.bottom

        if keys[pygame.K_DOWN]:
            player1.rect.y += cube_speed
            player2.rect.y += cube_speed
            for wall in walls:
                if collide_rect(player2, wall):
                    player2.rect.bottom = wall.rect.top
                if collide_rect(player1, wall):
                    player1.rect.bottom = wall.rect.top

                    for w in breaking_walls:
                        if collide_rect(player2, w):
                            w.kill()

                if len(vents) > 1:
                    if collide_rect(player1, vents.sprites()[0]):
                        player1.rect.bottom = vents.sprites()[1].rect.top
                        player1.rect.right = vents.sprites()[1].rect.bottom
                    elif collide_rect(player1, vents.sprites()[1]):
                        player1.rect.top = vents.sprites()[0].rect.bottom
                        player1.rect.right = vents.sprites()[0].rect.right

            if collide_rect(player1, player2):
                if player1.rect.y < player2.rect.y:
                    player1.rect.bottom = player2.rect.top
                else:
                    player2.rect.bottom = player1.rect.top



        if groupcollide(players, keys_group, False, True):
            for s in locked_walls:
                s.kill()

        # Clamp players to screen
        player1.rect.clamp_ip(screen.get_rect())
        player2.rect.clamp_ip(screen.get_rect())

        # Fill the screen with background
        screen.blit(background_surface, background_rect)

        # Draw the cubes
        all_sprites.update()
        all_sprites.draw(screen)

        if check_level_complete():
            text_surface = font.render('Level Complete', False, text_color)
            screen.blit(text_surface, screen.get_rect().center)
            pygame.display.flip()
            current_level, level_data, player1, player2, background_surface, background_rect = go_next_level(current_level)

    else:
        text_surface = font.render('Press space to play', False, text_color)
        screen.blit(text_surface, screen.get_rect(center=(500, 500)))
        if keys[pygame.K_SPACE]:
            current_level += 1
            background_surface = pygame.image.load(level_handler.level_background_path(current_level))
            background_rect = background_surface.get_rect(topleft=(0, 0))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
