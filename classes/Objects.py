from typing import Any
import pygame

# Initial data

global ichiban_cum, Hitbox, tile_size, kiryu

tile_size = (40, 40)

ichiban_cum = pygame.image.load('classes/ichiban.png')

kiryu = pygame.image.load('assets/sprites/kiryu.png')

Hitbox = {
    'safe': tile_size,
    'safe_ground': (40,20),
    'safe_wall': (20,40),
    'spike_vertical': (22, 8),
    'spike_sideways': (8, 22),
    'block': tile_size,
    'crystal': (30,30),
    'reverse': (30,30),
    'trampoline': (40,20),
    'strawberry': (30,30),
    'sticky': tile_size,
    'wood': (40, 7)
    }

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

    def __init__(self, x, y):
        self.hitbox = pygame.transform.scale(ichiban_cum, Hitbox['crystal'])
        self.hit_rect = self.hitbox.get_rect()
        self.hit_rect.x = x + 5
        self.hit_rect.y = y + 5
        self.data = [self.hit_rect, self.hitbox, True, 0]

    def update(self, screen):
        
        if self.data[2]:
            screen.blit(self.data[1], self.data[0])
        
        else:
            
            if self.data[3] < 250:
                self.data[3] += 1
                
                if self.data[3] >= 250:
                    self.data[3] = 0
                    self.data[2] = True

# Red Crystal (Reverse dash)

class Red_Crystal:

    global Hitbox

    def __init__(self, x, y):
        self.hitbox = pygame.transform.scale(ichiban_cum, Hitbox['crystal'])
        self.hit_rect = self.hitbox.get_rect()
        self.hit_rect.x = x + 5
        self.hit_rect.y = y + 5
        self.data = [self.hit_rect, self.hitbox, True, 0]

    def update(self, screen):
        
        if self.data[2]:
            screen.blit(self.data[1], self.data[0])
        
        else:
            
            if self.data[3] < 250:
                self.data[3] += 1
                
                if self.data[3] >= 250:
                    self.data[3] = 0
                    self.data[2] = True

# Trampoline tile

class Trampoline:

    global Hitbox

    def __init__(self, x, y):
        self.img = pygame.transform.scale(ichiban_cum, Hitbox['trampoline'])
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x 
        self.img_rect.y = y + 20
    
    def draw(self, screen):
        screen.blit(self.img, self.img_rect)

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

    def __init__(self, x, y):
        self.hitbox = pygame.transform.scale(ichiban_cum, Hitbox['block'])
        self.second = pygame.transform.scale(kiryu, Hitbox['block'])
        self.hit_rect = self.hitbox.get_rect()
        self.hit_rect.x = x 
        self.hit_rect.y = y
        self.data = [self.hit_rect, self.hitbox, self.second,  True, 0]
    
    def update(self, screen):
        if self.data[3]:
            screen.blit(self.data[1], self.data[0])
        else:
            self.data[4] += 1
            if self.data[4] <= 30:
                screen.blit(self.data[2], self.data[0])
            elif self.data[4] >= 250:
                self.data[4] = 0
                self.data[3] = True

# Strawberry 

class Strawberry:

    global Hitbox

    def __init__(self, x, y):
        self.image = pygame.transform.scale(ichiban_cum, Hitbox['strawberry'])
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.bolean = False
        
        # Display instances
        self.display_straw = False
        self.black_timer = 0
        self.reverse = False
        self.font = pygame.font.SysFont('arial', 30, True, True)
        self.black = pygame.Rect(0, 100, 0, 40)
        self.straw_rect = pygame.Rect(-40, 100, 0, 30)
        self.ichiban_cum_img = pygame.transform.scale(ichiban_cum, (30,30))
        self.ichiban_cum_rect = self.ichiban_cum_img.get_rect()
        self.ichiban_cum_rect.x = -80
        self.ichiban_cum_rect.y = 103

    
    def update(self, screen, strawberries):
        
        if not self.bolean:
            screen.blit(self.image, self.rect)

        if self.bolean:

            # Aux variables to display "collected"

            straw_print = f'x {strawberries}'
            straw_print_2 = self.font.render(straw_print, False, (255,255,255))

            # Display "collected" logic

            if self.display_straw:
                pygame.draw.rect(screen, (0,0,0), self.black)
                screen.blit(self.ichiban_cum_img, self.ichiban_cum_rect)
                screen.blit(straw_print_2, self.straw_rect)
                
                if self.black.width <= 100 and not self.reverse:
                    self.black.width += 10
                    self.ichiban_cum_rect.x+= 10
                    self.straw_rect.x+= 10
                    
                elif self.black.width >= 100 or self.reverse:
                    self.black_timer += 1
                    
                    if self.black_timer >= 120:
                        self.reverse = True
                        self.black.width -= 10
                        self.ichiban_cum_rect.x -= 10
                        self.straw_rect.x -= 10
                        
                        if self.black.width <= 0:
                            self.reverse = False
                            self.display_straw = False
                            self.black_timer = 0 


# Sticky tile

class Sticky:

    global Hitbox

    def __init__(self, x, y):
        self.image = pygame.transform.scale(ichiban_cum, Hitbox['sticky'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0,255,0), self.rect, 2)

# Moveable platform

class Moveable:

    global Hitbox

    def __init__(self, x, y, direction):
        self.image = pygame.transform.scale(ichiban_cum, Hitbox['wood'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.direction = direction

    def update(self, hitboxes, screen):

        if self.direction == 'Horizontal':
            self.rect.x += self.move_direction
       
        elif self.direction == 'Vertical':
            self.rect.y += self.move_direction
            
        for tile in hitboxes['hitbox']:
            
            if tile.colliderect(self.rect):
                self.move_direction = -(self.move_direction)

        for tile in hitboxes['block']:
            
            if tile[0].colliderect(self.rect):
                self.move_direction = -(self.move_direction)
        
        for tile in hitboxes['sticky']:
            
            if tile.colliderect(self.rect):
                self.move_direction = -(self.move_direction)
        
        for tile in hitboxes['trampoline']:
            
            if tile[1].colliderect(self.rect):
                self.move_direction = -(self.move_direction)   

        screen.blit(self.image, self.rect)  
