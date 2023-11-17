import pygame
import sys

from LevelHandler import LevelHandler, draw_map, load_collisions
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

    new_player2_x, new_player2_y = player2.rect.x, player2.rect.y

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Update cube positions based on key presses
    if keys[pygame.K_LEFT]:
        player1.rect.x -= cube_speed
        new_player2_x -= cube_speed
    if keys[pygame.K_RIGHT]:
        player1.rect.x += cube_speed
        new_player2_x += cube_speed
    if keys[pygame.K_UP]:
        player1.rect.y -= cube_speed
        new_player2_y -= cube_speed
    if keys[pygame.K_DOWN]:
        player1.rect.y += cube_speed
        new_player2_y += cube_speed

    # Check for collisions
    if player2.rect.collidelist(walls.sprites()) != -1:
        new_player2_x, new_player2_y = player2.rect.x, player2.rect.y

    # Update pos
    player2.rect.x = new_player2_x
    player2.rect.y = new_player2_y

    # Clamp players to screen
    player1.rect.clamp_ip(screen.get_rect())
    player2.rect.clamp_ip(screen.get_rect())

    # Fill the screen with white
    screen.fill(white)

    # Draw map
    draw_map(level_data, screen)

    # Draw the cubes
    all_sprites.update()
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
