from typing import Any
from Spritesheet import *
import pygame
from random import *
from Particles import *

# Initial data

global ichiban_cum, Hitbox, tile_size, kiryu

tile_size = (40, 40)

ichiban_cum = pygame.image.load('game/ichiban.png')

kiryu = pygame.image.load('assets/sprites/kiryu.png')

Hitbox = {
    'safe': tile_size,
    'safe_ground': (40,20),
    'safe_wall': (20,40),
    'spike_vertical': (20, 20),
    'spike_sideways': (20, 20),
    'block': tile_size,
    'crystal': (30,30),
    'reverse': (30,30),
    'trampoline': (40,20),
    'strawberry': (30,30),
    'sticky': tile_size,
    'wood': (32, 7)
    }

pygame.init()
screen = pygame.display.set_mode((800, 800))

# Sound effects

pygame.mixer.init()

sound_effects = {
    'spring': pygame.mixer.Sound('assets/sfx/spring.wav'),
    'green_crystal_get': pygame.mixer.Sound('assets/sfx/diamond_touch_01.wav'),
    'green_crystal_return': pygame.mixer.Sound('assets/sfx/diamond_return_01.wav'),
    'red_crystal_get': pygame.mixer.Sound('assets/sfx/diamond_touch_02.wav'),
    'red_crystal_return': pygame.mixer.Sound('assets/sfx/diamond_return_02.wav'),
    'blue_crystal_get': pygame.mixer.Sound('assets/sfx/diamond_touch_03.wav'),
    'blue_crystal_return': pygame.mixer.Sound('assets/sfx/diamond_return_03.wav'),
    'block_shake': pygame.mixer.Sound('assets/sfx/fallblock_shake.wav'),
    'block_broke': pygame.mixer.Sound('assets/sfx/platform_disintegrate_01.wav'),
    'strawberry_get': pygame.mixer.Sound('assets/sfx/strawberry_get.wav'),
    'strawberry_fly_flap': pygame.mixer.Sound('assets/sfx/strawberry_wingflap.wav'),
    'strawberry_fly': pygame.mixer.Sound('assets/sfx/strawberry_wingfly.wav'),
    'gold_strawberry': pygame.mixer.Sound('assets/sfx/strawberry_gold.wav')
}

# Volume changes

for x in sound_effects:
    sound_effects[x].set_volume(0.3)

# Classes

# Wood platform

class Platform:
    
    global Hitbox

    def __init__(self, x, y):
        self.image = pygame.transform.scale(ichiban_cum, Hitbox['wood'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Green Crystal (Extra dash)

class Green_Crystal:

    global Hitbox

    # Get sprites

    sprite = pygame.image.load('assets/sprites/spritesheet_green.png')
    sprites = SpriteSheet(sprite)
    frames_list = sprites.get_spritesheet(11, [16,16], (40,40), 'black')
    
    # Class

    def __init__(self, x, y, frames = frames_list):
        
        # Hitbox
        self.hitbox = pygame.transform.scale(ichiban_cum, Hitbox['crystal'])
        self.hit_rect = self.hitbox.get_rect()
        self.hit_rect.x = x + 5
        self.hit_rect.y = y + 5
        self.data = [self.hit_rect, self.hitbox, True, 0]

        # Image
        self.frames = frames
        self.img_rect = frames[0].get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.steps = len(self.frames)
        self.last_update = pygame.time.get_ticks()
        self.cooldown = 20
        self.animation_cd = 0
        self.frame = 0

        # Particles
        self.particles = Particles(self.hit_rect.centerx, self.hit_rect.centery, 10)
        self.color = 'green'

        # Sfx
        self.sound = [sound_effects['green_crystal_get'], sound_effects['green_crystal_return']]
        
    def update(self, screen):
        
        if self.data[2]:
           
           if self.animation_cd < 100:
               screen.blit(self.frames[0], self.img_rect)
               self.animation_cd += 1
            
           else:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.last_update >= self.cooldown:
                self.frame += 1
                self.last_update = current_time
                    
                if self.frame == len(self.frames):
                    self.frame = 0
                    self.animation_cd = 0
            
            screen.blit(self.frames[self.frame], self.img_rect)

        
        else:
            # Get sound
            if self.data[3] == 2:
                self.sound[0].play()
            
            if self.data[3] >= 2 and self.data[3] <= 5:     
                self.particles.explosion_particles(self.color, screen)
                self.particles.circle_explosion(screen, self.color)

            if self.data[3] >= 247 and self.data[3] <= 250:
                self.particles.circle_reverse(screen, self.color)

            if self.data[3] < 250:
                self.data[3] += 1

                if self.data[3] >= 250:
                    self.data[3] = 0
                    self.data[2] = True
                    self.sound[1].play()
                    self.particles.initial_position()

# Red Crystal (Reverse dash)

class Red_Crystal(Green_Crystal):

    global Hitbox

    # Get sprites

    sprite = pygame.image.load('assets/sprites/spritesheet_red.png')
    sprites = SpriteSheet(sprite)
    frames_list = sprites.get_spritesheet(12, [16,16], (40,40), 'black')
    
    # Class

    def __init__(self, x, y, frames = frames_list):
        
        # Inherit the green crystal class
        super().__init__(x, y, frames)
        
        # Change to red and sfx
        self.color = 'red'
        self.sound = [sound_effects['red_crystal_get'], sound_effects['red_crystal_return']]

# Blue Crystal (Flight)

class Blue_Crystal(Green_Crystal):
    
    global Hitbox

    # Get sprites

    sprite = pygame.image.load('assets/sprites/spritesheet_blue.png')
    sprites = SpriteSheet(sprite)
    frames_list = sprites.get_spritesheet(11, [16,16], (40,40), 'black')

    def __init__(self, x, y, frames = frames_list):
        super().__init__(x, y, frames)
        
        # Change color to blue and sfx
        self.color = 'blue'
        self.sound = [sound_effects['blue_crystal_get'], sound_effects['blue_crystal_return']]


# Trampoline tile

class Trampoline:

    global Hitbox

    # Get sprites

    sprites = pygame.image.load('assets/sprites/Jumper.png')
    spritesheet = SpriteSheet(sprites)
    frames_list = spritesheet.get_spritesheet(8, [24,16], (40,40), 'black')

    def __init__(self, x, y, frames_list = frames_list):
        
        # Hitboxes instances
        self.hit = pygame.transform.scale(ichiban_cum, Hitbox['trampoline'])
        self.hit_rect = self.hit.get_rect()
        self.hit_rect.x = x 
        self.hit_rect.y = y + 20
        self.bolean = False
        
        # Sprites and animations instances
        self.frames = frames_list
        self.img_rect = frames_list[0].get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.steps = len(self.frames)
        self.last_update = pygame.time.get_ticks()
        self.cooldown = 25
        self.frame = 0
    
    def update(self, screen):

        if not self.bolean:
            screen.blit(self.frames[0], self.img_rect)
        
        # Animation
        if self.bolean:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.last_update >= self.cooldown:
                self.frame += 1
                self.last_update = current_time
                
                if self.frame == 1:
                    sound_effects['spring'].play()
                    
                if self.frame == len(self.frames):
                    self.frame = 0
                    self.bolean = False
                
            screen.blit(self.frames[self.frame], self.img_rect)
            
# Spikes tile

class Spikes:

    global Hitbox

    def __init__(self, x, y, pos):
        if pos == 'Vertical':
            self.hitbox = pygame.transform.scale(ichiban_cum, Hitbox['spike_vertical'])
        
        elif pos == 'Sideways':
            self.hitbox = pygame.transform.scale(ichiban_cum, Hitbox['spike_sideways'])
        
        self.hit_rect = self.hitbox.get_rect()
        self.hit_rect.x = x 
        self.hit_rect.y = y

# Block tile

class Block:

    global Hitbox

    # Get sprites

    sprite = pygame.image.load('assets/sprites/spritesheet_block.png')
    sprites = SpriteSheet(sprite)
    frames_list = sprites.get_spritesheet(3, [8,8], (40,40), 'black')

    # Class

    def __init__(self, x, y, frames_list = frames_list):
        
        # Hitboxes
        self.hitbox = pygame.transform.scale(ichiban_cum, Hitbox['block'])
        self.hit_rect = self.hitbox.get_rect()
        self.hit_rect.x = x 
        self.hit_rect.y = y
        self.data = [self.hit_rect, True, 0]

        # Sprites
        self.frames = frames_list
        self.steps = len(self.frames)
        self.last_update = pygame.time.get_ticks()
        self.cooldown = 100
        self.frame = 0
        self.particles = Particles(self.hit_rect.bottomleft[0], self.hit_rect.bottomleft[1], 40)
        self.particles.random_position([0,40], [0,0])
    
    def update(self, screen, player_rect):
        if self.data[1]:
            screen.blit(self.frames[0], self.data[0])
        
        else:
            self.data[2] += 1

            if self.data[2] == 2:
                sound_effects['block_shake'].play()
            
            if self.data[2] <= 30:
                current_time = pygame.time.get_ticks()
                
                if current_time - self.last_update >= self.cooldown:
                    self.last_update = current_time
                    self.frames[1] = pygame.transform.rotate(self.frames[1], 90)
                        
                screen.blit(self.frames[1], self.hit_rect)
                self.particles.shaking_particles((0,0,0), screen)
                
            if self.data[2] == 30:
                sound_effects['block_broke'].play()
                self.particles.initial_position()
                self.particles.random_position([0,40], [-40,0])

            if self.data[2] >= 30 and self.data[2] <= 35:
                screen.blit(self.frames[2], self.hit_rect)
                self.particles.draw_particles(screen, (0,0,0))
            
            if self.data[2] >= 35 and self.data[2] <= 50:
                self.particles.add_gravity(randint(1,3), (0,0,0), screen)
            
            elif self.data[2] >= 250 and not self.hit_rect.colliderect(player_rect):
                self.data[2] = 0
                self.data[1] = True
                self.particles.initial_position()
                self.particles.random_position([0,40], [0,0])
                screen.blit(self.frames[2], self.hit_rect)

# Strawberry 

class Strawberry:

    global Hitbox

    # Get sprites

    sprite = pygame.image.load('assets/sprites/strawberry_spritesheet.png')
    sprites = SpriteSheet(sprite)
    frames_total = sprites.get_spritesheet(20, [18,16], (40,40), 'black')
    frames_display = frames_total[:10]
    frames_collected = frames_total[10:]
    
    # Class

    def __init__(self, x, y, frames_display = frames_display, frames_collected = frames_collected):
        
        # Hitbox instaces
        self.image = pygame.transform.scale(ichiban_cum, Hitbox['strawberry'])
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.bolean = False

        # Sprites instances
        self.img_rect = frames_display[0].get_rect()
        self.img_rect.x = x - 5
        self.img_rect.y = y - 5
        self.frames_collected = frames_collected
        self.frames_display = frames_display
        self.last_update = pygame.time.get_ticks()
        self.cooldown = 100
        self.frame = 0
        self.collected = False
        
        # Display instances
        self.display_straw = False
        self.black_timer = 0
        self.reverse = False
        self.font = pygame.font.Font('assets/ttf/pixel.ttf', 30)
        self.black = pygame.Rect(0, 100, 0, 40)
        self.straw_font = pygame.Rect(-70, 107, 0, 30)
        self.straw = pygame.transform.scale(frames_display[4], (50,50))
        self.straw_rect = self.straw.get_rect()
        self.straw_rect.x = -110
        self.straw_rect.y = 94

        # Sound instances
        self.sound = sound_effects['strawberry_get']

    
    def update(self, screen, strawberries):
        
        if not self.bolean:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.last_update >= self.cooldown:
                self.frame += 1
                self.last_update = current_time
                    
                if self.frame == len(self.frames_display):
                    self.frame = 0
            
            screen.blit(self.frames_display[self.frame], self.img_rect)

        if self.bolean:

            # Aux variables to display "collected"

            straw_print = f'x{strawberries}'
            straw_print_2 = self.font.render(straw_print, False, (255,255,255))

            # Display "collected" logic

            if self.display_straw:
                pygame.draw.rect(screen, (0,0,0), self.black)
                screen.blit(self.straw, self.straw_rect)
                screen.blit(straw_print_2, self.straw_font)
                
                if self.black.width <= 100 and not self.reverse:
                    self.black.width += 10
                    self.straw_font.x+= 10
                    self.straw_rect.x+= 10
                    
                elif self.black.width >= 100 or self.reverse:
                    self.black_timer += 1
                    
                    if self.black_timer >= 120:
                        self.reverse = True
                        self.black.width -= 10
                        self.straw_font.x -= 10
                        self.straw_rect.x -= 10
                        
                        if self.black.width <= 0:
                            self.reverse = False
                            self.display_straw = False
                            self.black_timer = 0 

            # Collect animation
            
            if self.collected:
                current_time = pygame.time.get_ticks()

                if self.frame == 0 and current_time - self.last_update >= self.cooldown:
                    self.sound.play()

                if current_time - self.last_update >= self.cooldown:
                    self.frame += 1
                    self.last_update = current_time
                        
                    if self.frame == len(self.frames_collected):
                        self.frame = 0
                        self.collected = False
                
                screen.blit(self.frames_collected[self.frame], self.img_rect)

# Flying strawberry

class Flying_Strawberry(Strawberry):
    
    global Hitbox

    # Get sprites

    sprite = pygame.image.load('assets/sprites/flying_straw.png')
    sprites = SpriteSheet(sprite)
    frames_list = sprites.get_spritesheet(10, [40,24], (80,60), 'black')
    
    # Class

    def __init__(self, x, y, frames = frames_list):
        # Inherit the strawberry class
        super().__init__(x, y)
        
        # Change sprites and image rect
        self.frames_display = frames
        self.img_rect.y -= 7
        self.img_rect.x -= 20
        
        # Fly instances
        self.has_dashed = False
        self.vel_y = 0

    def fly(self, screen):

        if self.has_dashed and self.vel_y != -1:

            if not self.bolean:

                self.vel_y += 0.25
                self.rect.y -= self.vel_y
                self.img_rect.y -= self.vel_y

                current_time = pygame.time.get_ticks()
                
                if current_time - self.last_update >= self.cooldown:
                    self.frame += 1
                    self.last_update = current_time
                        
                    if self.frame == len(self.frames_display):
                        self.frame = 0
                
                screen.blit(self.frames_display[self.frame], self.img_rect)

                if self.vel_y == 0.25:
                    sound_effects['strawberry_fly_flap'].play()
                    sound_effects['strawberry_fly'].play()

                if self.rect.y < -100:
                    self.vel_y = -1
                    self.has_dashed = False

# Golden strawberry

class Golden_Strawberry(Strawberry):

    # Get sprites

    sprite = pygame.image.load('assets/sprites/golden_straw.png')
    sprites = SpriteSheet(sprite)
    frames_list = sprites.get_spritesheet(8, [18,16], (40,40), 'black')
    
    # Class

    def __init__(self, x, y, frames = frames_list):
        # Inherit the strawberry class
        super().__init__(x, y)
        
        # Change sprites
        self.frames_display = frames
        
        # Change the sound 
        self.sound = sound_effects['gold_strawberry']

# Moveable platform

class Moveable:

    global Hitbox
    
    # Get sprites

    sprite = pygame.image.load('assets/sprites/Moving Platfrom_A.png')
    sprites = SpriteSheet(sprite)
    frames_list = sprites.get_spritesheet(10, [32,8], (48,14), 'black')
    
    # Class

    def __init__(self, x, y, direction, frames = frames_list):
        self.image = pygame.transform.scale(ichiban_cum, Hitbox['wood'])
        self.rect = self.image.get_rect()
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.rect.x = x + 8
        self.rect.y = y
        self.move_direction = 1.75
        self.move_counter = 0
        self.direction = direction

        # Sprites instances
        self.frames = frames
        self.steps = len(self.frames)
        self.last_update = pygame.time.get_ticks()
        self.cooldown = 25
        self.frame = 0

    def update(self, hitboxes, screen):

        if self.direction == 'Horizontal':
            self.rect.x += self.move_direction
            self.image_rect.x += self.move_direction
       
        elif self.direction == 'Vertical':
            self.rect.y += self.move_direction
            self.image_rect.y += self.move_direction
            
        for tile in hitboxes['hitbox']:
            
            if tile.colliderect(self.rect):
                self.move_direction = -(self.move_direction)

        for tile in hitboxes['block']:

            if tile.hit_rect.colliderect(self.rect) and tile.data[1]:
                self.move_direction = -(self.move_direction)
        
        if (self.rect.right >= 800 + 2 or self.rect.left <= 0) and self.direction == 'Horizontal':
            self.move_direction = -(self.move_direction)
        
        if (self.rect.y >= 800 or self.rect.y <= 0) and self.direction == 'Vertical':
            self.move_direction = -(self.move_direction)
        
        # Animation
    
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_update >= self.cooldown:
            self.frame += 1
            self.last_update = current_time
                
            if self.frame == len(self.frames):
                self.frame = 0
            
        screen.blit(self.frames[self.frame], self.image_rect)

# Flag cosmetic

class Flag:
    
    # Get sprites

    sprite = pygame.image.load('assets/sprites/flag.png')
    sprites = SpriteSheet(sprite)
    sprites_list = sprites.get_spritesheet(3, [8,8], [40,40], 'black')
    
    # Class

    def __init__(self, x, y, sprites_list = sprites_list):
        self.rect = sprites_list[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.sprites = sprites_list
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.cooldown = 100
    
    def update(self, screen):

        current_time = pygame.time.get_ticks()

        if current_time - self.last_update >= self.cooldown:
            self.frame += 1
            self.last_update = current_time
                
            if self.frame == len(self.sprites):
                self.frame = 0
        
        screen.blit(self.sprites[self.frame], self.rect)
