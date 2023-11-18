import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tile Map Editor")

# Define colors
white = (0, 0, 0)
black = (255, 255, 255)

# Define tile size and map
tile_size = 20
rows, cols = height // tile_size, width // tile_size
tile_map = [[0] * cols for _ in range(rows)]

# Load images
tile_image = pygame.Surface((tile_size, tile_size))
tile_image.fill(white)

pygame.key.set_repeat(1)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get the mouse position and update the tile map
                mouse_x, mouse_y = event.pos
                col = mouse_x // tile_size
                row = mouse_y // tile_size
                tile_map[row][col] = 1
            elif event.button == 3:  # Right mouse button
                # Get the mouse position and update the tile map
                mouse_x, mouse_y = event.pos
                col = mouse_x // tile_size
                row = mouse_y // tile_size
                tile_map[row][col] = 0

    keys = pygame.key.get_pressed()

    # Clear screen
    if keys[pygame.K_ESCAPE]:
        for row in range(rows):
            for col in range(cols):
                pygame.draw.rect(screen, black, (col * tile_size, row * tile_size, tile_size, tile_size))

    # Draw the tile map
    for row in range(rows):
        for col in range(cols):
            if tile_map[row][col] == 1:
                pygame.draw.rect(screen, white, (col * tile_size, row * tile_size, tile_size, tile_size))
            else:
                pygame.draw.rect(screen, black, (col * tile_size, row * tile_size, tile_size, tile_size))

    # Update the display
    pygame.display.flip()

    # Save tile map to a text file
    if pygame.key.get_pressed()[pygame.K_s]:  # Press 's' key to save
        with open("tile_map", "w") as file:
            for row in tile_map:
                file.write("".join(map(str, row)) + "\n")
        print("Tile map saved to tile_map")
