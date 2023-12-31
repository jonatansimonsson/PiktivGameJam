import pygame
import sys

from pygame.sprite import collide_rect, groupcollide

from LevelHandler import LevelHandler, load_collisions
from Player import Player

# Initialize Pygame
pygame.init()

# Set up display
width, height = 960, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Cubes")
font = pygame.font.SysFont("Comic Sans", 100)
small_font = pygame.font.SysFont("Comic Sans", 50, bold=True)
volume = 0.5


# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
text_color = (255, 0, 255)

tile_size = 24
cube_speed = 6
portal_activated = False

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
bee_goal = pygame.sprite.Group()
flower_goal = pygame.sprite.Group()
vents = pygame.sprite.Group()
keys_group = pygame.sprite.Group()
locked_walls = pygame.sprite.Group()
players = pygame.sprite.Group()
breaking_walls = pygame.sprite.Group()
portals = pygame.sprite.Group()

# Load level info and collisions
level_handler = LevelHandler()
level_handler.load_levels()
level_data = level_handler.load_map(level_handler.levels[0])
bee_spawn, flower_spawn = load_collisions(level_data, walls, all_sprites, bee_goal, flower_goal, vents, keys_group, locked_walls, breaking_walls, portals)
current_level = 0
background_surface = pygame.image.load(level_handler.level_background_path(current_level))
background_rect = background_surface.get_rect(topleft=(0, 0))
screen.blit(background_surface, background_rect)
music = pygame.mixer.Sound(level_handler.level_music_path(current_level))
music.set_volume(volume)
music.play(loops=-1)

# Create players
player1 = Player(red, tile_size, tile_size, bee_spawn, "Sprites/bee.png")
player2 = Player(blue, tile_size, tile_size, flower_spawn, "Sprites/flower.png")
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
        bee_spawn, flower_spawn = load_collisions(level_data, walls, all_sprites, bee_goal, flower_goal, vents, keys_group, locked_walls, breaking_walls, portals)
        player1 = Player(red, tile_size, tile_size, bee_spawn, "Sprites/bee.png")
        player2 = Player(blue, tile_size, tile_size, flower_spawn, "Sprites/flower.png")
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
                        sound = pygame.mixer.Sound('Sounds/WallBreak.wav')
                        sound.set_volume(volume)
                        sound.play()
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
                        sound = pygame.mixer.Sound('Sounds/WallBreak.wav')
                        sound.set_volume(volume)
                        sound.play()
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
                        sound = pygame.mixer.Sound('Sounds/WallBreak.wav')
                        sound.set_volume(volume)
                        sound.play()
                        w.kill()

                if len(vents) > 1:
                    if collide_rect(player1, vents.sprites()[0]):
                        sound = pygame.mixer.Sound('Sounds/Vent.wav')
                        sound.set_volume(volume)
                        sound.play()
                        player1.rect.bottom = vents.sprites()[1].rect.top
                        player1.rect.right = vents.sprites()[1].rect.right
                    elif collide_rect(player1, vents.sprites()[1]):
                        sound = pygame.mixer.Sound('Sounds/Vent.wav')
                        sound.set_volume(volume)
                        sound.play()
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
                        sound = pygame.mixer.Sound('Sounds/WallBreak.wav')
                        sound.set_volume(volume)
                        sound.play()
                        w.kill()

                if len(vents) > 1:
                    if collide_rect(player1, vents.sprites()[0]):
                        sound = pygame.mixer.Sound('Sounds/Vent.wav')
                        sound.set_volume(volume)
                        sound.play()
                        player1.rect.bottom = vents.sprites()[1].rect.top
                        player1.rect.right = vents.sprites()[1].rect.bottom
                    elif collide_rect(player1, vents.sprites()[1]):
                        sound = pygame.mixer.Sound('Sounds/Vent.wav')
                        sound.set_volume(volume)
                        sound.play()
                        player1.rect.top = vents.sprites()[0].rect.bottom
                        player1.rect.right = vents.sprites()[0].rect.right

            if collide_rect(player1, player2):
                if player1.rect.y < player2.rect.y:
                    player1.rect.bottom = player2.rect.top
                else:
                    player2.rect.bottom = player1.rect.top

        if groupcollide(players, keys_group, False, True):
            for s in locked_walls:
                sound = pygame.mixer.Sound('Sounds/Key.wav')
                sound.set_volume(volume)
                sound.play()
                s.kill()
        # Portals
        portal_collision = groupcollide(players, portals, False, False)
        if portal_collision and not portal_activated:
            sound = pygame.mixer.Sound('Sounds/TP.wav')
            sound.set_volume(volume)
            sound.play()
            player1_rect = player1.rect.topleft
            player1.rect.topleft = player2.rect.topleft
            player2.rect.topleft = player1_rect
            portal_activated = True
        elif not portal_collision:
            portal_activated = False

        # Clamp players to screen
        player1.rect.clamp_ip(screen.get_rect())
        player2.rect.clamp_ip(screen.get_rect())

        # Fill the screen with background
        screen.blit(background_surface, background_rect)

        # Draw the cubes
        all_sprites.update()
        all_sprites.draw(screen)

        if check_level_complete():
            if current_level == 4:
                current_level = 0
            sound = pygame.mixer.Sound('Sounds/LevelWin.wav')
            sound.set_volume(volume)
            sound.play()
            music.stop()
            music = pygame.mixer.Sound(level_handler.level_music_path(current_level+1))
            music.set_volume(volume)
            music.play(loops=-1)
            current_level, level_data, player1, player2, background_surface, background_rect = go_next_level(current_level)

    else:
        text_surface = small_font.render('Bee is smol, can fit into small places', False, red)
        screen.blit(text_surface, screen.get_rect(center=(500, 400)))
        text_surface = small_font.render('Flower is strong, try to break things', False, red)
        screen.blit(text_surface, screen.get_rect(center=(500, 450)))
        text_surface = small_font.render('Cooperate to reach symbiosis', False, red)
        screen.blit(text_surface, screen.get_rect(center=(500, 500)))
        text_surface = font.render('Press space to play', False, text_color)
        screen.blit(text_surface, screen.get_rect(center=(500, 700)))
        if keys[pygame.K_SPACE]:
            current_level += 1
            music.stop()
            music = pygame.mixer.Sound(level_handler.level_music_path(current_level))
            music.set_volume(volume)
            music.play(loops=-1)
            background_surface = pygame.image.load(level_handler.level_background_path(current_level))
            background_rect = background_surface.get_rect(topleft=(0, 0))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
