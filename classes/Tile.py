import pygame
from Objects import *

class Tile:
    
    # Initial data

    global tile_size, Hitbox

    tile_size = (40, 40)

    # Hitboxes
    
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



    def __init__(self, data):
        global Hitbox, tile_size
        
        # Lists of hitboxes and dictionary

        self.hitbox_list = []
        self.wood_list = []
        self.moveable_list = []
        self.grn_list= []
        self.red_list = []
        self.tramp_list = []
        self.spike_list = []
        self.block_list = []
        self.strawberry_list = []
        self.sticky_list = []

        self.tiles_dict = {
            'hitbox':  self.hitbox_list,
            'wood':  self.wood_list,
            'moveable': self.moveable_list,
            'green': self.grn_list,
            'red': self.red_list,
            'trampoline': self.tramp_list,
            'spike': self.spike_list,
            'block': self.block_list,
            'strawberry': self.strawberry_list,
            'sticky': self.sticky_list
        }
        
        # Tiles

        ichiban_cum = pygame.image.load('classes/ichiban.png')
        row_idx = 0 
        for row in data:
            col_idx = 0
            for tile in row:
                if tile == 1:  # Safe tile full
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0]
                    hitbox_rect.y = row_idx * tile_size[1]
                    self.hitbox_list.append(hitbox_rect)

                elif tile == 2:  # Safe tile ground 
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_ground'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0]
                    hitbox_rect.y = row_idx * tile_size[1] + 20 
                    self.hitbox_list.append(hitbox_rect)

                elif tile == 3: # Safe tile ground reverse
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_ground'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0]
                    hitbox_rect.y = row_idx * tile_size[1]
                    self.hitbox_list.append(hitbox_rect)
                
                elif tile == 4: # Safe tile wall left
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_wall'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0]
                    hitbox_rect.y = row_idx * tile_size[1] 
                    self.hitbox_list.append(hitbox_rect)

                elif tile == 5: # Safe tile wall right
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_wall'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0] + 20
                    hitbox_rect.y = row_idx * tile_size[1] 
                    self.hitbox_list.append(hitbox_rect)

                elif tile == 6:  # Spike tile up
                    spike = Spikes(col_idx * tile_size[0] + 12, row_idx * tile_size[1] + 30, 'Vertical')
                    self.spike_list.append(spike.hit_rect)
                
                elif tile == 7: # Spike tile down
                    spike = Spikes(col_idx * tile_size[0] + 12, row_idx * tile_size[1] + 2, 'Vertical')
                    self.spike_list.append(spike.hit_rect)

                elif tile == 8: # Spike tile left
                    spike = Spikes(col_idx * tile_size[0] + 2, row_idx * tile_size[1] + 7, 'Sideways')
                    self.spike_list.append(spike.hit_rect)

                elif tile == 9: # Spike tile right
                    spike = Spikes(col_idx * tile_size[0] + 30, row_idx * tile_size[1] + 7, 'Sideways')
                    self.spike_list.append(spike.hit_rect)  

                elif tile == 10: # Spike with ground 
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_ground'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0]
                    hitbox_rect.y = row_idx * tile_size[1] + 20 
                    self.hitbox_list.append(hitbox_rect)
                    spike = Spikes(hitbox_rect.x + 6, hitbox_rect.y - 10, 'Vertical')
                    self.spike_list.append(spike.hit_rect)

                elif tile == 11: # Spike with ground reverse
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_ground'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0]
                    hitbox_rect.y = row_idx * tile_size[1]
                    self.hitbox_list.append(hitbox_rect)
                    spike = Spikes(hitbox_rect.x + 7, hitbox_rect.y + 22, 'Vertical')
                    self.spike_list.append(spike.hit_rect)
                
                elif tile == 12: # Spike left wall
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_wall'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0]
                    hitbox_rect.y = row_idx * tile_size[1] 
                    self.hitbox_list.append(hitbox_rect)
                    spike = Spikes(hitbox_rect.x + 23, hitbox_rect.y + 12, 'Sideways')
                    self.spike_list.append(spike.hit_rect)
                
                elif tile == 13: # Spike right wall
                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_wall'])
                    hitbox_rect = hitbox.get_rect()
                    hitbox_rect.x = col_idx * tile_size[0] + 20
                    hitbox_rect.y = row_idx * tile_size[1] 
                    self.hitbox_list.append(hitbox_rect)
                    spike = Spikes(hitbox_rect.x - 10, hitbox_rect.y + 12, 'Sideways')
                    self.spike_list.append(spike.hit_rect)

                elif tile == 14:  # Block 
                    block = Block(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.block_list.append(block)
                
                elif tile == 15:  # Green Crystal 
                    grn_crystal = Green_Crystal(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.grn_list.append(grn_crystal)
                
                elif tile == 16:  # Red Crystal
                    red_crystal = Red_Crystal(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.red_list.append(red_crystal)
                
                elif tile == 17:  # Trampoline
                    trampoline = Trampoline(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.tramp_list.append(trampoline)
                
                elif tile == 18:  # Strawberry
                    strawberry = Strawberry(col_idx * tile_size[0] + 5, row_idx * tile_size[1] + 5)
                    self.strawberry_list.append(strawberry)
                
                elif tile == 19:  # Moveable Horizontal
                    moveable = Moveable(col_idx * tile_size[0], row_idx* tile_size[1] + 33, 'Horizontal')
                    self.moveable_list.append(moveable)

                elif tile == 20: # Moveable Vertical
                    moveable = Moveable(col_idx * tile_size[0], row_idx* tile_size[1] + 33, 'Vertical')
                    self.moveable_list.append(moveable)
                
                elif tile == 21:  # Sticky
                    sticky = Sticky(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.sticky_list.append(sticky)
                
                elif tile == 22: # Wood
                    wood = Platform(col_idx * tile_size[0], row_idx * tile_size[1] + 33)
                    self.wood_list.append(wood.rect)
                    
                col_idx += 1
            row_idx += 1

    def draw(self,screen): # Show Hitboxes (For debug purposes)
        
        for hitbox in self.hitbox_list:
            pygame.draw.rect(screen, (255,255,255), hitbox, 2)

        for wood in self.wood_list:
            pygame.draw.rect(screen, (255,255,255), wood, 2)
        
        for spike in self.spike_list:
            pygame.draw.rect(screen, (255,0,0), spike, 2)
        
        for green in self.grn_list:
            pygame.draw.rect(screen, (30, 255, 0), green.hit_rect, 2)
        
        for red in self.red_list:
            pygame.draw.rect(screen, (255,0,0), red.hit_rect, 2)
        
        for straw in self.strawberry_list:
            pygame.draw.rect(screen, (255,50,0), straw.rect, 2)
        
        for trampoline in self.tramp_list:
            pygame.draw.rect(screen, (255,255,255), trampoline.rect, 2)

        for sticky in self.sticky_list:
            pygame.draw.rect(screen, (0,255,0), sticky.rect, 2)
        
        for moveable in self.moveable_list:
            pygame.draw.rect(screen, (255,255,255), moveable.rect, 2)
        
        for block in self.block_list:
            pygame.draw.rect(screen, (0,0,0), block.hit_rect, 2)
        