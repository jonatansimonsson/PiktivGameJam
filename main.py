import pygame
import sys

from pygame.sprite import spritecollide, collide_rect

from LevelHandler import LevelHandler, load_collisions
from Sprite import Sprite
from Player import Player

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Cubes")

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

tile_size = 20
cube_speed = 5

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()

player1 = Player(red, 20, 20, [0, 0])
player2 = Player(blue, 20, 20, [300, 300])
player1.add(all_sprites)
player2.add(all_sprites)

level_handler = LevelHandler()
level_handler.load_levels()
level_data = level_handler.load_map(level_handler.levels[0])

load_collisions(level_data, [all_sprites, walls])

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Update cube positions based on key presses
    if keys[pygame.K_LEFT]:
        player1.rect.x -= cube_speed
        player2.rect.x -= cube_speed
        for wall in walls:
            if collide_rect(player2, wall):
                player2.rect.left = wall.rect.right
            if collide_rect(player1, wall):
                player1.rect.left = wall.rect.right

    if keys[pygame.K_RIGHT]:
        player1.rect.x += cube_speed
        player2.rect.x += cube_speed
        for wall in walls:
            if collide_rect(player2, wall):
                player2.rect.right = wall.rect.left
            if collide_rect(player1, wall):
                player1.rect.right = wall.rect.left

    if keys[pygame.K_UP]:
        player1.rect.y -= cube_speed
        player2.rect.y -= cube_speed
        for wall in walls:
            if collide_rect(player2, wall):
                player2.rect.top = wall.rect.bottom
            if collide_rect(player1, wall):
                player1.rect.top = wall.rect.bottom

    if keys[pygame.K_DOWN]:
        player1.rect.y += cube_speed
        player2.rect.y += cube_speed
        for wall in walls:
            if collide_rect(player2, wall):
                player2.rect.bottom = wall.rect.top
            if collide_rect(player1, wall):
                player1.rect.bottom = wall.rect.top

    all_sprites.update()

    # Clamp players to screen
    player1.rect.clamp_ip(screen.get_rect())
    player2.rect.clamp_ip(screen.get_rect())

    # Fill the screen with white
    screen.fill(white)

    # Draw the cubes
    all_sprites.update()
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
