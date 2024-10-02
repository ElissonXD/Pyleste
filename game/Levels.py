import pygame
import pygame.freetype
import pygame.freetype
import pygame.freetype
from Player import *
from Tile import *
from random import *
from Particles import *

# Initial data function

def initial_data(level, x, y):
    
    global width, height, player, screen, clock, shake, shake_timer, snow, game_over, run, show_level, show_timer, font, print_1, print_2, print_rect, sfx, first_steps

    # Screen, fps, player data

    width = 800
    height = 800
    player = Player(x, y)
    player.jumped = True

    # Inits

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Effects

    shake = [0,0]
    shake_timer = 0
    snow = Particles(0, 0, 80)
    snow.random_position([0,800], [0,800])

    # Sfx

    wind_1 = pygame.mixer.Sound('assets/sfx/wind_1.wav')
    wind_2 = pygame.mixer.Sound('assets/sfx/wind_2.wav')
    start_level = pygame.mixer.Sound('assets/sfx/start_level.wav')
    wind_1.set_volume(0.1)
    wind_2.set_volume(0.1)

    sfx = {'wind1': wind_1,
           'wind2': wind_2,
           'start_level': start_level}

    # Music

    first_steps = pygame.mixer.Sound('assets/music/first_steps.mp3')

    first_steps.set_volume(0.3)

    # Loops

    game_over = False
    run = True

    # Show level

    show_level = True
    show_timer = 100
    font = pygame.font.Font('assets/ttf/pixel.ttf', 40)
    print_1 = f'{level}m'
    print_2 = font.render(print_1, False, (255,255,255))
    print_rect = pygame.Rect(350, 105, 200, 20)
    
    # Timer and death

    timer = 0 # work later
    deaths = 0 # work later

# Update

def update(tiles, strawberries, next_level, game_over, player, snow_vel):

    global show_level, show_timer, clock, shake, shake_timer, snow

    # Show level logic

    if show_level:
        show_timer -= 1

        pygame.draw.rect(screen, 'black', (0, 100, 800, 50))
        screen.blit(print_2, print_rect)
        
        if show_timer == 99:
            sfx['start_level'].play()

        if show_timer <= 0:
            show_level = False

    # Game over and strawberries
    game_over,strawberries = player.controls(tiles.tiles_dict, screen, game_over,strawberries)
    
    # Pass to the next level

    if player.rect.y < -10:
        next_level = True

    # Shake logic

    # Dash shake
    if player.screen_shake and player.is_dashing:
        shake_timer += 1
        shake[0] = randint(-4,4)
        shake[1] = randint(-4,4)

        if shake_timer >= 14 or not player.is_dashing:
            player.screen_shake = False
            shake = [0, 0]
            shake_timer = 0

    # Crystal shake
    elif player.screen_shake:
        shake_timer += 1
        shake[0] = randint(-2,2)
        shake[0] = randint(-2,2)

        if shake_timer >= 10:
            player.screen_shake = False
            shake = [0, 0]
            shake_timer = 0
    
    #tiles.draw(screen)
    # Particles, clock and shake

    clock.tick(60)

    snow.snowing('white', screen, snow_vel)

    screen.blit(pygame.transform.scale(screen,(800,800)), shake)
    #tiles.draw(screen)
    pygame.display.update()

    return game_over, strawberries, next_level

# Levels

def level_1(strawberries):

    # Initial data
    initial_data(100, 50, 250)

    global width, height, player, screen, clock, shake, shake_timer, snow, game_over, run, show_level, show_timer, font, print_1, print_2, print_rect, sfx, musics

    level_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
    
    # Set background 
    
    tiles = Tile(level_data)
    background = pygame.image.load('assets/maps/level 1.png')
    background_scale = pygame.transform.scale(background, (800, 800))
    back_rect = background_scale.get_rect()
    back_rect = pygame.Rect(0, 0, 45, 45)

    # Strotage stawberries and next level

    initial_straws = strawberries
    next_level = False

    # Wind and music

    sfx['wind1'].play(-1)
    first_steps.play(-1)

    # Game loop

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
    
        screen.blit(background_scale, back_rect)
        
        # Restart
        if game_over and player.go_timer > 50:
            
            level_1(initial_straws)
        
        # Update
        else: 
            game_over, strawberries, next_level = update(tiles, strawberries, next_level, game_over, player, [-5, 7])
            
            if next_level:

                level_2(strawberries)

    pygame.quit()

def level_2(strawberries):

    # Initial data
        
        initial_data(200, 20, 500)

        global width, height, player, screen, clock, shake, shake_timer, snow, game_over, run, show_level, show_timer, font, print_1, print_2, print_rect

        level_data = [
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 6, 6, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 23, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 23, 23, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 19, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 8, 0, 0, 0, 9, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 8, 0, 0, 0, 9, 1, 0, 0]
    ]
        
        # Set background 
        
        tiles = Tile(level_data)
        background = pygame.image.load('assets/maps/level 2.png')
        background_scale = pygame.transform.scale(background, (800, 800))
        back_rect = background_scale.get_rect()
        back_rect = pygame.Rect(0, 0, 45, 45)

        # Strotage stawberries and next level

        initial_straws = strawberries
        next_level = False

        # Game loop

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
        
            screen.blit(background_scale, back_rect)
            
            # Restart
            if game_over and player.go_timer > 50:
                
                level_2(initial_straws)
            
            # Update
            else: 
                game_over, strawberries, next_level = update(tiles, strawberries, next_level, game_over, player, [-5, 7])

                if next_level:

                    level_2(strawberries)

        pygame.quit()