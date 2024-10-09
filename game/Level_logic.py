import pygame
import pygame.freetype
import pygame.freetype
import pygame.freetype
from Player import *
from Tile import *
from random import *
from Particles import *
from Level_data import *

# Time
global secs, minutes, hours
secs = 0
minutes = 0
hours = 0

# Initial data function

def initial_data(level, x, y, deaths):
    
    global width, height, player, screen, clock, shake, shake_timer, snow, game_over, run, show_level, show_timer, font, print_1, print_2, print_rect, sfx, first_steps
    global death_img, death_rect, death_print_aux, death_print_rect
    global timer_print_aux, timer_rect

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
    font = pygame.font.Font('assets/ttf/pixel.ttf', 45)
    print_1 = f'{level}m'
    print_2 = font.render(print_1, False, (255,255,255))
    print_rect = pygame.Rect(350, 105, 200, 20)
    
    # Timer print

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font_timer = pygame.font.Font('assets/ttf/pixel.ttf', 40)
    timer_print = f'{hours}:{str(minutes).zfill(2)}:{str(secs).zfill(2)}'
    timer_print_aux = font_timer.render(timer_print, False, 'white')
    timer_rect = pygame.Rect(330, 0, 200, 20)
    
    # Deaths

    deaths = deaths
    death_img = pygame.image.load('assets/sprites/skull.png')
    death_img = pygame.transform.scale(death_img, (30,30))
    death_rect = death_img.get_rect()
    death_rect.x = 361
    death_rect.y = 148
    death_print = f'x{deaths}'
    font_death = pygame.font.Font('assets/ttf/pixel.ttf', 30)
    death_print_aux = font_death.render(death_print, False, (255,255,255))
    death_print_rect = pygame.Rect(393, 150, 200, 20)

# Update

def update(tiles, strawberries, next_level, game_over, player, snow_vel, fake = [False]):

    global show_level, show_timer, clock, shake, shake_timer, snow

    # Game over and strawberries
    game_over,strawberries = player.controls(tiles.tiles_dict, screen, game_over,strawberries)
    
    # Fake background
    
    if fake[0]:
        screen.blit(fake[1], fake[2])

    # Pass to the next level

    if player.rect.y < -10:
        next_level = True

    # Update flag animation

    for flag in tiles.tiles_dict['flag']:
        flag.update(screen)

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
    
    # Particles, clock and shake

    clock.tick(60)

    snow.snowing('white', screen, snow_vel)

    screen.blit(pygame.transform.scale(screen,(800,800)), shake)

    # Show level, deaths and time

    if show_level:
        show_timer -= 1
        
        # Level and deaths
        pygame.draw.rect(screen, 'black', (0, 100, 800, 80))
        screen.blit(print_2, print_rect)
        screen.blit(death_img, death_rect)
        screen.blit(death_print_aux, death_print_rect)

        # Timer
        pygame.draw.rect(screen, 'black', (310, 0, 200, 50))
        screen.blit(timer_print_aux, timer_rect)

        
        if show_timer == 99:
            sfx['start_level'].play()

        if show_timer <= 0:
            show_level = False

    #tiles.draw(screen)
    pygame.display.update()

    return game_over, strawberries, next_level

# Levels

def level_logic(strawberries, deaths, data, index):

    # Initial data
    initial_data(data[index][0], data[index][1], data[index][2], deaths)

    global width, height, player, screen, clock, shake, shake_timer, snow, game_over, run, show_level, show_timer, font, print_1, print_2, print_rect, sfx, musics
    global secs, minutes, hours

    # Music

    if index == 1:
        sfx['wind1'].play(-1)
        first_steps.play(-1)

    # Strotage stawberries and next level

    initial_straws = strawberries
    next_level = False

    # Game loop

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            
            if event.type == pygame.USEREVENT:
                secs += 1
                
                if secs == 60:
                    secs = 0
                    minutes += 1
                    
                    if minutes == 60:
                        minutes = 0
                        hours += 1
    
        screen.blit(data[index][3], data[index][4])
        
        # Restart
        if game_over and player.go_timer > 50:
            deaths += 1
            level_logic(initial_straws, deaths, data, index)
        
        # Update
        else:

            game_over, strawberries, next_level = update(data[index][5], strawberries, next_level, game_over, player, [-5, 7], data[index][6])
            
            if next_level:
                index += 1
                level_logic(strawberries, deaths, data, index)
            
    pygame.quit()