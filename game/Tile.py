import pygame
from Objects import *

class Tile:

    # Class

    def __init__(self, data):
        
        # Lists of hitboxes and dictionary

        self.hitbox_list = []
        self.wood_list = []
        self.moveable_list = []
        self.grn_list= []
        self.red_list = []
        self.blue_list = []
        self.tramp_list = []
        self.spike_list = []
        self.block_list = []
        self.strawberry_list = []
        self.straw_fly_list = []
        self.golden_list = []
        self.flag_list = []

        self.tiles_dict = {
            'hitbox':  self.hitbox_list,
            'wood':  self.wood_list,
            'moveable': self.moveable_list,
            'green': self.grn_list,
            'red': self.red_list,
            'blue': self.blue_list,
            'trampoline': self.tramp_list,
            'spike': self.spike_list,
            'block': self.block_list,
            'strawberry': self.strawberry_list,
            'flying_straw': self.straw_fly_list,
            'golden_straw': self.golden_list,
            'flag': self.flag_list
        }
        
        # Tiles

        ichiban_cum = pygame.image.load('game/ichiban.png')
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

                elif tile == 2:  # Spike tile up
                        spike = Spikes(col_idx * tile_size[0] + 8, row_idx * tile_size[1] + 20, 'Vertical')
                        self.spike_list.append(spike.hit_rect)
                    
                elif tile == 3: # Spike tile down
                    spike = Spikes(col_idx * tile_size[0] + 8, row_idx * tile_size[1], 'Vertical')
                    self.spike_list.append(spike.hit_rect)

                elif tile == 4: # Spike tile left
                    spike = Spikes(col_idx * tile_size[0], row_idx * tile_size[1] + 12, 'Sideways')
                    self.spike_list.append(spike.hit_rect)

                elif tile == 5: # Spike tile right
                    spike = Spikes(col_idx * tile_size[0] + 20, row_idx * tile_size[1] + 12, 'Sideways')
                    self.spike_list.append(spike.hit_rect)

                elif tile == 6:  # Block 
                    block = Block(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.block_list.append(block)
                
                elif tile == 7:  # Green Crystal 
                    grn_crystal = Green_Crystal(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.grn_list.append(grn_crystal)
                
                elif tile == 8:  # Red Crystal
                    red_crystal = Red_Crystal(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.red_list.append(red_crystal)
                
                elif tile == 9: # Blue Crystal
                    blue_crystal = Blue_Crystal(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.blue_list.append(blue_crystal)
                
                elif tile == 10:  # Trampoline
                    trampoline = Trampoline(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.tramp_list.append(trampoline)
                
                elif tile == 11:  # Strawberry
                    strawberry = Strawberry(col_idx * tile_size[0] + 5, row_idx * tile_size[1] + 5)
                    self.strawberry_list.append(strawberry)
                
                elif tile == 12:  # Flying Strawberry
                    strawberry = Flying_Strawberry(col_idx * tile_size[0] + 5, row_idx * tile_size[1] + 5)
                    self.straw_fly_list.append(strawberry)
                
                elif tile == 13:  # Moveable Horizontal
                    moveable = Moveable(col_idx * tile_size[0], row_idx* tile_size[1] + 33, 'Horizontal')
                    self.moveable_list.append(moveable)

                elif tile == 14: # Moveable Vertical
                    moveable = Moveable(col_idx * tile_size[0], row_idx* tile_size[1] + 33, 'Vertical')
                    self.moveable_list.append(moveable)
                
                elif tile == 15: # Wood
                    wood = Platform(col_idx * tile_size[0], row_idx * tile_size[1] + 33)
                    self.wood_list.append(wood.rect)
                
                elif tile == 16: # Flag
                    flag = Flag(col_idx * tile_size[0], row_idx * tile_size[1])
                    self.flag_list.append(flag)
                
                elif tile == 17: # Golden Strawberry
                    golden = Golden_Strawberry(col_idx * tile_size[0] + 5, row_idx * tile_size[1] + 5)
                    self.golden_list.append(golden)
                    
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
        
        for blue in self.blue_list:
            pygame.draw.rect(screen, (0,0,255), blue.hit_rect, 2)
        
        for straw in self.strawberry_list:
            pygame.draw.rect(screen, (255,50,0), straw.rect, 2)
        
        for straw in self.straw_fly_list:
            pygame.draw.rect(screen, (255,50,0), straw.rect, 2)
        
        for trampoline in self.tramp_list:
            pygame.draw.rect(screen, (255,255,255), trampoline.hit_rect, 2)
        
        for moveable in self.moveable_list:
            pygame.draw.rect(screen, (255,255,255), moveable.rect, 2)
        
        for block in self.block_list:
            pygame.draw.rect(screen, (0,0,0), block.hit_rect, 2)

#################################################################

# SAVING CODE IF GONNA USE IT

#               elif tile == 2:  # Safe tile ground 
#                   hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_ground'])
#                    hitbox_rect = hitbox.get_rect()
#                    hitbox_rect.x = col_idx * tile_size[0]
#                    hitbox_rect.y = row_idx * tile_size[1] + 20 
#                    self.hitbox_list.append(hitbox_rect)
#
#                elif tile == 3: # Safe tile ground reverse
#                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_ground'])
#                    hitbox_rect = hitbox.get_rect()
#                    hitbox_rect.x = col_idx * tile_size[0]
#                    hitbox_rect.y = row_idx * tile_size[1]
#                    self.hitbox_list.append(hitbox_rect)
#                
#                elif tile == 4: # Safe tile wall left
#                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_wall'])
#                    hitbox_rect = hitbox.get_rect()
#                    hitbox_rect.x = col_idx * tile_size[0]
#                    hitbox_rect.y = row_idx * tile_size[1] 
#                    self.hitbox_list.append(hitbox_rect)
#
#                elif tile == 5: # Safe tile wall right
#                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_wall'])
#                    hitbox_rect = hitbox.get_rect()
#                    hitbox_rect.x = col_idx * tile_size[0] + 20
#                    hitbox_rect.y = row_idx * tile_size[1] 
#                    self.hitbox_list.append(hitbox_rect)
#                 
#                elif tile == 10: # Spike with ground 
#                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_ground'])
#                    hitbox_rect = hitbox.get_rect()
#                    hitbox_rect.x = col_idx * tile_size[0]
#                    hitbox_rect.y = row_idx * tile_size[1] + 20 
#                    self.hitbox_list.append(hitbox_rect)
#                    spike = Spikes(hitbox_rect.x + 6, hitbox_rect.y - 10, 'Vertical')
#                    self.spike_list.append(spike.hit_rect)
#
#                elif tile == 11: # Spike with ground reverse
#                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_ground'])
#                    hitbox_rect = hitbox.get_rect()
#                    hitbox_rect.x = col_idx * tile_size[0]
#                    hitbox_rect.y = row_idx * tile_size[1]
#                    self.hitbox_list.append(hitbox_rect)
#                    spike = Spikes(hitbox_rect.x + 7, hitbox_rect.y + 22, 'Vertical')
#                    self.spike_list.append(spike.hit_rect)
#                
#                elif tile == 12: # Spike left wall
#                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_wall'])
#                    hitbox_rect = hitbox.get_rect()
#                    hitbox_rect.x = col_idx * tile_size[0]
#                    hitbox_rect.y = row_idx * tile_size[1] 
#                    self.hitbox_list.append(hitbox_rect)
#                    spike = Spikes(hitbox_rect.x + 23, hitbox_rect.y + 12, 'Sideways')
#                    self.spike_list.append(spike.hit_rect)
#                
#                elif tile == 13: # Spike right wall
#                    hitbox = pygame.transform.scale(ichiban_cum, Hitbox['safe_wall'])
#                    hitbox_rect = hitbox.get_rect()
#                    hitbox_rect.x = col_idx * tile_size[0] + 20
#                    hitbox_rect.y = row_idx * tile_size[1] 
#                    self.hitbox_list.append(hitbox_rect)
#                    spike = Spikes(hitbox_rect.x - 10, hitbox_rect.y + 12, 'Sideways')
#                    self.spike_list.append(spike.hit_rect)