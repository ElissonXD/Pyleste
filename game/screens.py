import pygame
import pygame.freetype
import pygame.freetype
import pygame.freetype
from Player import *
from Tile import *
from random import *
from Particles import *
from Level_data import *

# Music and Sfx

global sfx, musics

# Sfx

wind_1 = pygame.mixer.Sound('assets/sfx/wind_1.wav')
wind_2 = pygame.mixer.Sound('assets/sfx/wind_2.wav')
start_level = pygame.mixer.Sound('assets/sfx/start_level.wav')
start_game = pygame.mixer.Sound('assets/sfx/start.wav')
end = pygame.mixer.Sound('assets/sfx/end.wav')
wind_1.set_volume(0.1)
wind_2.set_volume(0.1)

sfx = {
    'wind1': wind_1,
    'wind2': wind_2,
    'start_level': start_level,
    'start_game': start_game,
    'end': end
        }

# Music

prologue = pygame.mixer.Sound('assets/music/prologue.mp3')
first_steps = pygame.mixer.Sound('assets/music/first_steps.mp3')
first_steps_b_side = pygame.mixer.Sound('assets/music/first_steps_b side.mp3')
reach_summit = pygame.mixer.Sound('assets/music/reach_summit.mp3')

prologue.set_volume(0.3)
first_steps.set_volume(0.3)
first_steps_b_side.set_volume(0.3)
reach_summit.set_volume(0.3)

musics = {
    'prologue': prologue,
    'first_steps': first_steps,
    'first_steps_b side': first_steps_b_side,
    'reach_summit': reach_summit
    }

# Music boleans

global music1, music2, music3

music1 = False
music2 = False
music3 = False

# Initial data function

def initial_data(level, x, y, deaths):
    
    global width, height, player, screen, clock, shake, shake_timer, snow, game_over, run, show_level, show_timer, font, print_1, print_2, print_rect, sfx, musics
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

    # Loops

    game_over = False
    run = True

    # Show level

    show_level = True
    show_timer = 100
    font = pygame.font.Font('assets/ttf/pixel.ttf', 45)
    
    if deaths == '???':
        print_1 = f'{level}'
    
    else:
        print_1 = f'{level}m'

    print_2 = font.render(print_1, False, (255,255,255))
    print_rect = pygame.Rect(325, 105, 200, 20)
    
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
    death_rect.x = 351
    death_rect.y = 148
    death_print = f'x{deaths}'
    font_death = pygame.font.Font('assets/ttf/pixel.ttf', 30)
    death_print_aux = font_death.render(death_print, False, (255,255,255))
    death_print_rect = pygame.Rect(383, 150, 200, 20)

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

    return game_over, strawberries, next_level

# Levels

def level_logic(strawberries, deaths, levels, data, index):

    # Initial data
    initial_data(data[index][0], data[index][1], data[index][2], deaths)

    global width, height, player, screen, clock, shake, shake_timer, snow, game_over, run, show_level, show_timer, font, print_1, print_2, print_rect, sfx, musics
    global secs, minutes, hours
    global music1, music2, music3 

    # Music

    if index <= 13 and not music1:
        sfx['wind1'].play(-1)
        musics['first_steps'].play(-1)
        
        music1 = True
    
    if index > 13 and index <= 26 and not music2:
        musics['first_steps'].stop()
        
        musics['first_steps_b side'].play(-1)
        
        music2 = True
    
    if index > 26 and index <= 39 and not music3:
        musics['first_steps_b side'].stop()
        sfx['wind1'].stop()
        
        musics['reach_summit'].play(-1)
        sfx['wind2'].play(-1)

        music3 = True
    
    # Strotage stawberries, next level and initial tile

    initial_tiles = Tile(data[index][7])
    initial_straws = strawberries
    next_level = False

    # Skip level timer

    skip_timer = 100

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
            data[index][5] = initial_tiles
            level_logic(initial_straws, deaths, levels, data, index)
        
        # Update
        else:
            
            if index <= 13: # Slow snow
                snow_vel = [-5,7]

            if index > 13 and index <= 26: # Medium snow
                snow_vel = [-10,14]
            
            if index > 26 and index <= 40: # Fast Snow
                snow_vel = [-14, 21]

            game_over, strawberries, next_level = update(data[index][5], strawberries, next_level, game_over, player, snow_vel, data[index][6])
            
            pygame.display.update()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_s]:
                skip_timer -= 1

                if skip_timer == 0:
                    next_level = True
                    levels -= 1
            
            else:
                skip_timer = 100

            if next_level:
                index += 1
                levels += 1
                
                if index == 40:
                    summit(strawberries, deaths, levels, data)
                
                else:
                    level_logic(strawberries, deaths, levels, data, index)
            
    pygame.quit()


# Summit level

def summit(strawberries, deaths, levels,  data):
    
    # Initial data
    
    initial_data(data[40][0], data[40][1], data[40][2], '???')

    global width, height, player, screen, clock, shake, shake_timer, snow, game_over, run, show_level, show_timer, font, print_1, print_2, print_rect, sfx, musics
    global secs, minutes, hours
    global music1, music2, music3

    # Music

    musics['reach_summit'].fadeout(5000)

    # Tiles 

    tiles = Tile(data[40][7])
    
    # Results 

    ended = False
    back_to_menu = False
    final_straws = strawberries
    final_deaths = deaths
    
    # Fonts

    font_z = pygame.font.Font('assets/ttf/pixel.ttf', 20)

    # Show results logic

    show_1 = False
    show_2 = False
    show_3 = False
    show_timer_image = 100

    # Prints

    good_job = 'Good job!'
    print_gj = font.render(good_job, False, (255,255,255))
    results = 'Results'
    print_results = font.render(results, False, (255,255,255))
    thank_you = 'Thanks for playing!'
    print_ty = font.render(thank_you, False, (255,255,255))
    total_straws = f'x {final_straws + 1} / 40'
    print_straws = font.render(total_straws, False, (255,255,255))
    total_deaths = f'x {final_deaths}'
    print_deaths = font.render(total_deaths, False, (255,255,255))
    total_levels = f'x {levels} / 40'
    print_levels = font.render(total_levels, False, (255,255,255))

    effect_timer = 60
    press_z = 'Press Z to continue'
    press_esc = 'Press ESC to return to the title screen'
    print_z = font_z.render(press_z, False, (255,255,255))
    print_esc = font_z.render(press_esc, False, (255,255,255))

    # Images and rects
    # Images
    straw_final_image = pygame.image.load('assets/sprites/strawberry.png')
    flag_final_image = pygame.image.load('assets/sprites/clear.png')
    death_final_image = pygame.image.load('assets/sprites/skull.png')
    time_final_image = pygame.image.load('assets/sprites/time.png')
    
    # Scales and image rects

    straw_scale = pygame.transform.scale(straw_final_image, (50, 50))
    flag_scale = pygame.transform.scale(flag_final_image, (50, 50))
    death_scale = pygame.transform.scale(death_final_image, (50, 50))
    time_scale = pygame.transform.scale(time_final_image, (50, 50))
    
    straw_rect = straw_scale.get_rect()
    flag_rect = flag_scale.get_rect()
    death_rect_2 = death_scale.get_rect()
    time_rect = time_scale.get_rect()

    time_rect.x = 175
    flag_rect.x = 175
    straw_rect.x = 170
    death_rect_2.x = 170
    
    time_rect.y = 125
    flag_rect.y = 250
    straw_rect.y = 375
    death_rect_2.y = 500

    # Rects
    # Black Squares
    black_square_1 = pygame.Rect(150, 50, 500, 200)
    black_square_2 = pygame.Rect(100, 50, 600, 600)
    black_square_3 = pygame.Rect(50, 50, 700, 200)

    # Prints rects
    gj_rect = pygame.Rect(275,100, 100, 100)
    
    results_rect = pygame.Rect(300, 50, 100, 100)
    total_time_rect = pygame.Rect(250, 125, 100, 100)
    total_straws_rect = pygame.Rect(225, 375, 100, 100)
    total_deaths_rect = pygame.Rect(225, 500, 100, 100)
    total_levels_rect = pygame.Rect(225, 250, 100, 100)

    thank_you_rect = pygame.Rect(120, 100, 100, 100)
    z_rect_1 = pygame.Rect(285, 200, 50, 50)
    z_rect_2 = pygame.Rect(125, 600, 50, 50)
    esc_rect = pygame.Rect(155, 200, 50, 50)

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
    
        screen.blit(data[40][3], data[40][4])

        game_over, strawberries, back_to_menu = update(tiles, strawberries, back_to_menu, game_over, player, [-14, 21], data[40][6])


        if tiles.tiles_dict['golden_straw'][0].bolean and not ended:
            
            finished_time = f'{hours}:{str(minutes).zfill(2)}:{str(secs).zfill(2)}'
            print_time = font.render(finished_time, False, (255,255,255))

            ended = True
        
        if ended and show_timer_image > 0:
            show_timer_image -= 1

        if show_timer_image <= 0:

            if not show_1 and not show_2 and not show_3:
                show_1 = True
                show_timer_image = 10
                sfx['end'].play()
            
        if show_1:
            pygame.draw.rect(screen, 'black', black_square_1)
            screen.blit(print_gj, gj_rect)

            if show_timer_image == 0:
                key = pygame.key.get_pressed()
                
                effect_timer -= 1

                if effect_timer == -61:
                    effect_timer = 60

                if effect_timer > -60 and effect_timer < 0:
                    screen.blit(print_z, z_rect_1)

                if key[pygame.K_z]:
                    show_2 = True
                    show_1 = False
                    show_timer_image = 100
                    sfx['end'].play()
        
        if show_2:
            pygame.draw.rect(screen, 'black', black_square_2)
            screen.blit(print_results, results_rect)

            screen.blit(time_scale, time_rect)
            screen.blit(flag_scale, flag_rect)
            screen.blit(straw_scale, straw_rect)
            screen.blit(death_scale, death_rect_2)

            screen.blit(print_time, total_time_rect)
            screen.blit(print_levels, total_levels_rect)
            screen.blit(print_straws, total_straws_rect)
            screen.blit(print_deaths, total_deaths_rect)

            if show_timer_image == 0:
                key = pygame.key.get_pressed()

                effect_timer -= 1

                if effect_timer == -61:
                    effect_timer = 60

                if effect_timer > -60 and effect_timer < 0:
                    screen.blit(print_z, z_rect_2)

                if key[pygame.K_z]:
                    show_2 = False
                    show_3 = True
                    show_timer_image = 100
                    sfx['end'].play()
        
        if show_3:
            pygame.draw.rect(screen, 'black', black_square_3)
            screen.blit(print_ty, thank_you_rect)

            if show_timer_image == 0:
                key = pygame.key.get_pressed()

                effect_timer -= 1

                if effect_timer == -61:
                    effect_timer = 60

                if effect_timer > -60 and effect_timer < 0:
                    screen.blit(print_esc, esc_rect)

                if key[pygame.K_ESCAPE]:
                    title_screen()

        pygame.display.update()
    
    pygame.quit()

# Title screen

def title_screen():

    # Reset Time, music and sfx
    
    global secs, minutes, hours
    secs = 0
    minutes = 0
    hours = 0
    global music1, music2, music3
    music1 = False
    music2 = False
    music3 = False

    sfx['wind2'].stop()

    # Initial data 

    pygame.init()
    pygame.mixer.init()

    run = True
    background_title = pygame.image.load('assets/screens/title_screen.png')
    back_rect = pygame.Rect(0, 0, 45, 45)

    width = 800
    height = 800
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    snow = Particles(0, 0, 80)
    snow.random_position([0,800], [0,800])

    # Begin logic

    started = False
    start_timer = 100

    black_rect = pygame.Rect(0, 900, 800, 800)
    black_rect_timer = 100

    # Fonts

    font = pygame.font.Font('assets/ttf/pixel.ttf', 80)
    font_xc = pygame.font.Font('assets/ttf/pixel.ttf', 40)

    # Texts

    pyleste = 'Pyleste'
    press_x_or_c = 'Press X or C to begin'

    # Text Render

    print_py = font.render(pyleste, False, 'light blue')
    print_xc = font_xc.render(press_x_or_c, False, 'white')

    # Text rects

    pyleste_rect = pygame.Rect(220, 370, 200, 200)
    press_rect = pygame.Rect(140, 650, 50, 50)

    # Text effect timer

    start_effect = 60

    # Music

    musics['prologue'].play(-1)

    # Main loop

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        screen.blit(background_title, back_rect)

        screen.blit(print_py, pyleste_rect)

        start_effect -= 1

        if not started:
            
            if start_effect == -61:
                start_effect = 60

            if start_effect > -60 and start_effect < 0:
                screen.blit(print_xc, press_rect)
        
        if started:
        
            if start_timer == 100:
                sfx['start_game'].play()
                musics['prologue'].fadeout(1000)
            
            start_timer -= 1

            if start_effect == -11:
                start_effect = 10

            if start_effect > -10 and start_effect < 0:
                screen.blit(print_xc, press_rect)

        snow.snowing('white', screen, [-5,7])

        if start_timer <= 0:

            if black_rect.y != 0:
                black_rect.y -= 10
            
            else:
                black_rect_timer -= 1
            
            if black_rect_timer <= 0:

                level_logic(0, 0, 1, all_levels, 1)

            pygame.draw.rect(screen, 'black', black_rect)

        key = pygame.key.get_pressed()

        if (key[pygame.K_x] or key[pygame.K_c]) and not started:
            
            started = True
            start_effect = 10

        pygame.display.update()
    
    pygame.quit()