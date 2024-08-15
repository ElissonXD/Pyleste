import pygame

class Tile:
    
    global tile_size, Hitbox

    tile_size = (35, 40)

    # Hitboxes
    
    Hitbox = {
    'safe': tile_size,
    'spike': (20, 25),
    'block': tile_size,
    'crystal': (30,30),
    'reverse': (30,30),
    'trampoline': tile_size,
    'strawberry': (30,30),
    'movable': tile_size,
    'sticky': tile_size,
    }

    # Images (work later)

    def __init__(self, data):
        global Hitbox, tile_size
        
        self.map_list = []

        ichiban_cum = pygame.image.load('classes/ichiban.png')
        row_idx = 0 
        for row in data:
            col_idx = 0
            for tile in row:
                if tile == 1:  # Safe
                    img = pygame.transform.scale(ichiban_cum, Hitbox['safe'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)
                
                elif tile == 2:  # Spike
                    img = pygame.transform.scale(ichiban_cum, Hitbox['spike'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)
                
                elif tile == 3:  # Block
                    img = pygame.transform.scale(ichiban_cum, Hitbox['block'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)
                
                elif tile == 4:  # Crystal
                    img = pygame.transform.scale(ichiban_cum, Hitbox['crystal'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)
                
                elif tile == 5:  # Reverse
                    img = pygame.transform.scale(ichiban_cum, Hitbox['reverse'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)
                
                elif tile == 6:  # Trampoline
                    img = pygame.transform.scale(ichiban_cum, Hitbox['trampoline'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)
                
                elif tile == 7:  # Strawberry
                    img = pygame.transform.scale(ichiban_cum, Hitbox['strawberry'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)
                
                elif tile == 8:  # Movable
                    img = pygame.transform.scale(ichiban_cum, Hitbox['movable'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)
                
                elif tile == 9:  # Sticky
                    img = pygame.transform.scale(ichiban_cum, Hitbox['sticky'])
                    img_rect = img.get_rect()
                    img_rect.x = col_idx * tile_size[0]
                    img_rect.y = row_idx * tile_size[1]
                    tile = (img, img_rect)
                    self.map_list.append(tile)

                col_idx += 1
            row_idx += 1

    def draw(self,screen):
        
        for tile in self.map_list:
            screen.blit(tile[0], tile[1])