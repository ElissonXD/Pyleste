import pygame
from Spritesheet import *
from Particles import *

class Player:

    # Initial data

    global gravity, left_dash, right_dash, up_dash, down_dash, right_WJs, left_WJs
    gravity = 0.5
    left_dash = False
    right_dash = False
    up_dash = False
    down_dash = False
    right_WJs = 0
    left_WJs = 0

    pygame.init()
    screen = pygame.display.set_mode((800, 800))

    # Get sprites

    # Player sprites
    sprite_red = pygame.image.load('assets/sprites/madeline_red.png') # Red sprites
    sprites_red = SpriteSheet(sprite_red)
    frames_red_all = []
    frames_red_all_flipped = []
    sprite_blue = pygame.image.load('assets/sprites/madeline_blue.png') # Blue sprites
    sprites_blue = SpriteSheet(sprite_blue)
    frames_blue_all = []
    frames_blue_all_flipped = []
    sprite_green = pygame.image.load('assets/sprites/madeline_green.png') # Green sprites
    sprites_green = SpriteSheet(sprite_green)
    frames_green_all = []
    frames_green_all_flipped = []

    for x in range(7):
        frames_red_all.append(sprites_red.get_image(x, 8, 8, (30,30), (0,0,0)))
        frames_red_all_flipped.append(pygame.transform.flip(sprites_red.get_image(x, 8, 8, (30,30), (0,0,0)), True, False))
        frames_blue_all.append(sprites_blue.get_image(x, 8, 8, (30,30), (0,0,0)))
        frames_blue_all_flipped.append(pygame.transform.flip(sprites_blue.get_image(x, 8, 8, (30,30), (0,0,0)), True, False))
        frames_green_all.append(sprites_green.get_image(x, 8, 8, (30,30), (0,0,0)))
        frames_green_all_flipped.append(pygame.transform.flip(sprites_green.get_image(x, 8, 8, (30,30), (0,0,0)), True, False))

    all_sprites = {
                   'red': frames_red_all,
                   'red_flipped': frames_red_all_flipped,
                   'blue': frames_blue_all,
                   'blue_flipped': frames_blue_all_flipped,
                   'green': frames_green_all,
                   'green_flipped': frames_green_all_flipped,
                    }

    # Sound effects
    
    pygame.mixer.init()

    sfx = {
        'dash_red': pygame.mixer.Sound('assets/sfx/dash_red.wav'),
        'jump': pygame.mixer.Sound('assets/sfx/jump.wav'),
        'jump_wall': pygame.mixer.Sound('assets/sfx/jump_wall.wav'),
        'death': pygame.mixer.Sound('assets/sfx/death.wav')
    }

    # Change volume

    for sound in sfx:
        sfx[sound].set_volume(0.5)

    def __init__(self, x, y, all_sprites = all_sprites, sfx = sfx):
        
        # Coordenates and rect
        self.img = pygame.transform.scale(all_sprites['red'][0], (30,30))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = 0
        self.vel_y = 0
        self.go_timer = 0

        # All sprites and flip bolean
        self.all_sprites = all_sprites
        self.flip = False
        self.flip_right = 0
        self.flip_left = 0
        self.touched_ground = 0
        self.sprite = 'red'

        # Walking frames
        self.all_walking = {
                            'walk_red': all_sprites['red'][:4],
                            'walk_red_flipped': all_sprites['red_flipped'][:4],
                            'walk_blue': all_sprites['blue'][:4],
                            'walk_blue_flipped': all_sprites['blue_flipped'][:4],
                            'walk_green': all_sprites['green'][:4],
                            'walk_green_flipped': all_sprites['green_flipped'][:4]
                            }
        self.can_walk = False
        self.frames_present = self.all_walking['walk_red']
        self.frame_walking = 0
        self.cooldown = 5
        
        # Looking up and down frames
        self.all_looking = {
                            'look_red': all_sprites['red'][5:],
                            'look_red_flipped': all_sprites['red_flipped'][5:],
                            'look_blue': all_sprites['blue'][5:],
                            'look_blue_flipped': all_sprites['blue_flipped'][5:],
                            'look_green': all_sprites['green'][5:],
                            'look_green_flipped': all_sprites['green_flipped'][5:]
                            }
        self.looking_present = self.all_looking['look_red']

        # Wall jump frames
        self.all_wj = {
                            'wall_red': all_sprites['red'][4],
                            'wall_red_flipped': all_sprites['red_flipped'][4],
                            'wall_blue': all_sprites['blue'][4],
                            'wall_blue_flipped': all_sprites['blue_flipped'][4],
                            'wall_green': all_sprites['green'][4],
                            'wall_green_flipped': all_sprites['green_flipped'][4]
                            }
        self.wj_present = self.all_wj['wall_red']
        
        # Particles
        self.dash_particles = Particles(self.rect.bottomleft[0], self.rect.bottomleft[1], 30)
        self.wall_slide_particles = Particles(self.rect.bottomleft[0], self.rect.bottomleft[1] - 5, 20)
        self.walking_particles = Particles(self.rect.bottomleft[0], self.rect.bottomleft[1], 10)
        self.land_particles =  Particles(self.rect.centerx, self.rect.centery + 15, 6)
        self.death_particle = Particles(self.rect.centerx, self.rect.centery, 8)

        # Sfx
        self.sfx = sfx

        # Allow screen shake
        self.screen_shake = False
        
        # Wall Jump
        self.can_WJ = False
        self.is_WJ = False
        self.left_WJ = False
        self.right_WJ = False
        self.stay = 0
        self.WJ_timer = 0
        self.WJ_height = 5

        # Jump
        self.jump = 7
        self.jump_timer = 0
        self.tramp_height = -10
        self.coyote_timer = 0
        self.jumped = False
        self.is_jumping = False
        
        # Dash
        self.dash_speed = 7
        self.dash_time = 10
        self.dash = True
        self.reverse = False
        self.reverse_timer = 0
        self.is_dashing = False
        self.dash_timer = 0

        # Floating
        self.floating_timer = 300
        self.is_floating = False

    def controls(self, tiles, screen, game_over, strawberries):
        
        global gravity, left_dash, right_dash, down_dash, up_dash, right_WJs, left_WJs

        if not self.is_floating:
            self.dx = 0
       
        self.dy = 0
        down = False
        left = False
        right = False
        up = False

        # Game over

        if not game_over: 

            # Controls
        
            key = pygame.key.get_pressed()
            
            if key[pygame.K_LEFT] and not self.is_dashing and not self.is_WJ:
                
                if self.reverse_timer > 0 and right_dash:
                    self.reverse_timer -= 1
                
                else:

                    if self.is_floating:
                        self.dx -= 1
                    
                    else:
                        self.dx -= 5

                    left = True
                    self.cooldown -= 1
                    self.flip = True
            
            if key[pygame.K_RIGHT] and not self.is_dashing and not self.is_WJ:
                
                if self.reverse_timer > 0 and left_dash:
                    self.reverse_timer -= 1
                
                else:
                    
                    if self.is_floating:
                        self.dx += 1
                    
                    else:
                        self.dx += 5
                    
                    right = True
                    self.cooldown -= 1
                    self.flip = False
            
            if key[pygame.K_UP]:
                up = True

                if not left and not right:
                    screen.blit(self.looking_present[1], self.rect)
            
            if key[pygame.K_x] and not self.jumped:
                self.vel_y = -self.jump
                self.jumped = True
                self.is_jumping = True
            
            if key[pygame.K_DOWN] and not self.is_floating:
                down = True
            
            # Jump Logic

            if self.is_jumping:
                self.jump_timer += 1
                
                if self.jump_timer == 1:
                    self.sfx['jump'].play()

                if self.jump_timer >= 15:
                    self.is_jumping = False
                    self.jump_timer = 0
                
                screen.blit(self.looking_present[1], self.rect)

            # Is Wall Jumping

            if self.is_WJ:
                self.WJ_timer += 1
                
                if self.WJ_timer == 1:
                    self.sfx['jump_wall'].play()

                if self.right_WJ:
                    self.dx = -5 
                    
                    if right_WJs == 1:
                        self.vel_y = -self.WJ_height
                    
                    else:
                        self.vel_y = -3
                    
                    if 'red' in self.sprite:
                        screen.blit(self.all_walking['walk_red_flipped'][2], self.rect)
                    
                    elif 'blue' in self.sprite:
                        screen.blit(self.all_walking['walk_blue_flipped'][2], self.rect)
                    
                    elif 'green' in self.sprite:
                        screen.blit(self.all_walking['walk_green_flipped'][2], self.rect)
                
                elif self.left_WJ:
                    self.dx = 5
                    
                    if left_WJs == 1:
                        self.vel_y = -self.WJ_height
                    
                    else:
                        self.vel_y = -3

                    if 'red' in self.sprite:
                        screen.blit(self.all_walking['walk_red'][2], self.rect)
                    
                    elif 'blue' in self.sprite:
                        screen.blit(self.all_walking['walk_blue'][2], self.rect)
                    
                    elif 'green' in self.sprite:
                        screen.blit(self.all_walking['walk_green'][2], self.rect)  
                
                if self.WJ_timer >= 15:
                    self.WJ_timer = 0
                    self.is_WJ = False
                    self.right_WJ = False
                    self.left_WJ = False
                
            # Dash Logic

            if key[pygame.K_c] and self.dash and not self.is_dashing and not self.is_floating:
                self.is_dashing = True
                self.dash = False
                self.is_jumping = False
                self.jump_timer = 0
                self.jumped = True
                self.is_WJ = False
                self.WJ_timer = 0
                self.screen_shake = True
                
                if left:
                    
                    if self.reverse:
                        self.dx = self.dash_speed
                        right_dash = True
                    
                    else:
                        self.dx = -self.dash_speed
                        left_dash = True
                
                if right:
                    
                    if self.reverse:
                        self.dx = -self.dash_speed
                        left_dash = True     
                    
                    else:
                        self.dx = self.dash_speed
                        right_dash = True
                
                if down:
                    
                    if self.reverse:
                        self.vel_y = -self.dash_speed 
                        up_dash = True
                    
                    else:
                        self.vel_y = self.dash_speed 
                        down_dash = True
                
                if up:
                    
                    if self.reverse:
                        self.vel_y = self.dash_speed 
                        down_dash = True                
                    
                    else:
                        self.vel_y = -self.dash_speed 
                        up_dash = True
                
                if not left and not up and not right and not down:
                    
                    if self.reverse:
                        self.vel_y = self.dash_speed 
                        down_dash = True                     
                    
                    else:
                        self.vel_y = -self.dash_speed 
                        up_dash = True
                
                self.reverse = False
                self.reverse_timer = 10

            # Dash animation    
            if self.is_dashing:
                self.dash_timer += 1
                
                if left_dash:
                    self.dx = -self.dash_speed - 1
                    
                    if not up_dash and not down_dash:
                        self.vel_y = 0
                
                if right_dash:
                    self.dx = self.dash_speed + 1
                    
                    if not up_dash and not down_dash:
                        self.vel_y = 0
                
                if (right_dash or left_dash) and not up_dash and not down_dash:
                    screen.blit(self.frames_present[3], self.rect)
                
                if down_dash:
                    screen.blit(self.looking_present[0], self.rect)

                if up_dash:
                    screen.blit(self.looking_present[1], self.rect)
                
                if self.dash_timer == 1:

                    if up_dash:
                        self.dash_particles.set_position(self.rect.bottomleft[0], self.rect.bottomleft[1])
                        self.dash_particles.random_position((0,30), (0,0))
                    
                    elif left_dash:
                        self.dash_particles.set_position(self.rect.centerx + 15, self.rect.centery)
                        self.dash_particles.random_position((0,0), (-15,15))

                    elif right_dash:
                        self.dash_particles.set_position(self.rect.centerx - 15, self.rect.centery)
                        self.dash_particles.random_position((0,0), (-15,15))
                    
                    elif down_dash:
                        self.dash_particles.set_position(self.rect.topleft[0], self.rect.topleft[1])
                        self.dash_particles.random_position((0,30), (0,0))
                    
                    self.sfx['dash_red'].play()

                self.dash_particles.dash(self.vel_y, self.dx, (255,255,255), screen)

                if self.dash_timer >= 15:
                    self.is_dashing = False
                    self.dash_timer = 0
                    left_dash = False
                    right_dash = False
                    up_dash = False
                    down_dash = False
                    self.dash_particles.initial_position()

            # Floating logic
            
            if self.is_floating:
                self.vel_y = -3
                self.floating_timer -= 1

                if not left and not right:

                    if self.dx > 0:
                        self.dx -= 0.25
                    
                    elif self.dx < 0:
                        self.dx += 0.25
                    
                    else:
                        self.dx = 0

                if self.dx <= -5:
                    self.dx = -5
                
                if self.dx >= 5:
                    self.dx = 5

                if self.floating_timer <= 0:
                    self.is_floating = False

            # Gravity

            if not self.is_dashing and not self.is_jumping and not self.can_WJ and not self.is_WJ and not self.is_floating:
                self.vel_y += gravity
                
                if self.reverse_timer > 0:
                    self.reverse_timer -= 1 
                
                else: 
                    
                    if down: 
                        self.vel_y = 9

                        if not right and not left and not up:
                            screen.blit(self.looking_present[0], self.rect)
                    
                    else:
                        
                        if self.vel_y >= 7:
                            self.vel_y = 7
            
            self.dy += self.vel_y

            # Coyote Jump
            if self.coyote_timer > 0:
                self.coyote_timer -= 1
            
            else:
                self.jumped = True
            
            self.can_WJ = False
            self.can_walk = False
                
            # Collision with tiles

            for tile in tiles['hitbox']:
                
                # X direction
                if tile.colliderect(self.rect.x + self.dx, self.rect.y, 30, 30):
                    self.dx = 0
                    self.is_WJ = False
                    self.WJ_timer = 0

                    # Wall Jump Logic
                    if right and self.vel_y >= 0:
                        self.can_WJ = True

                        if self.stay >= 10:
                            self.vel_y = 2
                        
                        else:
                            self.vel_y = 0
                            self.stay += 1
                        
                        screen.blit(self.wj_present, self.rect)

                        if (key[pygame.K_x]) and not self.is_WJ:
                            self.is_WJ = True
                            self.right_WJ = True
                            self.left_WJ = False
                            self.jumped = True
                            right_WJs += 1
                            left_WJs = 0
                            
                            if right_WJs == 1:
                                self.stay = 0
                    
                    elif left and self.vel_y >= 0:
                        self.can_WJ = True
            
                        if self.stay >= 10:
                            self.vel_y = 2
                        
                        else:
                            self.vel_y = 0
                            self.stay += 1
                        
                        screen.blit(self.wj_present, self.rect)
                        
                        if (key[pygame.K_x]) and not self.is_WJ:
                            self.is_WJ = True
                            self.left_WJ = True
                            self.right_WJ = False
                            self.jumped = True
                            right_WJs = 0
                            left_WJs += 1
                            
                            if left_WJs == 1:
                                self.stay = 0
    
                # Y direction 
                if tile.colliderect(self.rect.x, self.rect.y + self.dy, 30, 30):
                    
                    if self.vel_y < 0:
                        self.dy = tile.bottom - self.rect.top
                        self.is_dashing = False
                        self.is_jumping = False
                        self.dash_timer = 0
                        self.jump_timer = 0
                        self.is_WJ = False
                        self.WJ_timer = 0
                        self.vel_y = 0
                    
                    elif self.vel_y >= 0: 
                        self.dy = tile.top - self.rect.bottom
                        self.dash = True
                        self.jumped = False
                        self.vel_y = 2
                        self.can_walk = True
                        right_WJs = 0
                        left_WJs = 0 
                        self.coyote_timer = 3

            # Colision with objects

            for tile in tiles['wood']: # Floating platforms
                
                if tile.colliderect(self.rect.x, self.rect.y + self.dy, 30, 30):
                    
                    if self.rect.bottom < tile.centery:
                        
                        if self.vel_y >= 0:
                            self.dy = 0
                            self.rect.bottom = tile.top
                            self.dash = True
                            self.vel_y = 2
                            self.can_walk = True
                            self.jumped = False
                            right_WJs = 0
                            left_WJs = 0 
                            self.coyote_timer = 3

            for tile in tiles['green']: # Green Crystals
                
                if tile.data[2]:
                    
                    if tile.data[0].colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30) and not self.dash:
                        self.dash = True
                        tile.data[2] = False
                        self.screen_shake = True
                
                tile.update(screen)

            for tile in tiles['red']: # Red Crystals
                
                if tile.data[2]:
                    
                    if tile.data[0].colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30) and not self.dash:
                        self.reverse = True
                        self.dash = True
                        tile.data[2] = False
                        self.screen_shake = True
                
                tile.update(screen)
            
            for tile in tiles['blue']: # Blue Crystals
                
                if tile.data[2]:
                    
                    if tile.data[0].colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30):
                        self.is_floating = True
                        self.dash = True
                        tile.data[2] = False
                        self.screen_shake = True
                        self.floating_timer = 300
                
                tile.update(screen)

            for tile in tiles['trampoline']: # Trampoline
                
                # Y direction

                if tile.hit_rect.colliderect(self.rect.x, self.rect.y + self.dy, 30, 30):
                    self.vel_y = self.tramp_height
                    self.dash = True
                    self.jumped = True
                    self.is_jumping = True
        
                    tile.bolean = True
                
                # X direction

                if tile.hit_rect.colliderect(self.rect.x + self.dx, self.rect.y, 30, 30):
                    self.vel_y = self.tramp_height
                    self.dash = True
                    self.jumped = True
                    self.is_jumping = True
        
                    tile.bolean = True
            
                tile.draw(screen)

            for tile in tiles['spike']: # Spikes
                
                if tile.colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30):
                    game_over = True

            for tile in tiles['block']: # Blocks
                
                if tile.data[2] <= 30:

                    # X direction
                    
                    if tile.data[0].colliderect(self.rect.x + self.dx, self.rect.y, 30, 30):
                        self.dx = 0
                        tile.data[1] = False

                        # Wall Jump Logic
                        
                        self.is_WJ = False
                        self.WJ_timer = 0

                        # Wall Jump Logic
                        if right and self.vel_y >= 0:
                            self.can_WJ = True
            
                            if self.stay >= 10:
                                self.vel_y = 2
                            
                            else:
                                self.vel_y = 0
                                self.stay += 1

                            if (key[pygame.K_x]) and not self.is_WJ:
                                self.is_WJ = True
                                self.right_WJ = True
                                self.left_WJ = False
                                self.jumped = True
                                right_WJs += 1
                                left_WJs = 0
                                if right_WJs == 1:
                                    self.stay = 0
                        
                        elif left and self.vel_y >= 0:
                            self.can_WJ = True
                        
                            if self.stay >= 10:
                                self.vel_y = 2
                            
                            else:
                                self.vel_y = 0
                                self.stay += 1
                            
                            if (key[pygame.K_x]) and not self.is_WJ:
                                self.is_WJ = True
                                self.left_WJ = True
                                self.right_WJ = False
                                self.jumped = True
                                self.stay = 0
                                right_WJs = 0
                                left_WJs += 1
                                if left_WJs == 1:
                                    self.stay = 0
                    
                    # Y direction 
                    
                    if tile.data[0].colliderect(self.rect.x, self.rect.y + self.dy, 30, 30):
                        
                        if self.vel_y < 0:
                            tile.data[1] = False
                            self.dy = tile.data[0].bottom - self.rect.top
                            self.is_dashing = False
                            self.is_jumping = False
                            self.dash_timer = 0
                            self.jump_timer = 0
                            self.is_WJ = False
                            self.WJ_timer = 0
                            self.vel_y = 0
                        
                        elif self.vel_y >= 0:
                            tile.data[1] = False
                            self.dy = tile.data[0].top - self.rect.bottom
                            self.dash = True
                            self.jumped = False
                            self.vel_y = 2
                            self.can_walk = True
                            right_WJs = 0
                            left_WJs = 0 
                            self.coyote_timer = 3
            
                tile.update(screen, (self.rect.x, self.rect.y + self.dy, 30, 30))

            for tile in tiles['strawberry']:  # Strawberry
                
                if not tile.bolean:
                    
                    if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30):
                        tile.bolean = True
                        tile.display_straw = True
                        strawberries += 1
                        tile.frame = 0
                        tile.collected = True
                
                tile.update(screen,strawberries)
            
            for tile in tiles['flying_straw']:

                if not tile.bolean:

                    if not self.is_dashing:

                        if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30):
                            tile.bolean = True
                            tile.display_straw = True
                            strawberries += 1
                            tile.frame = 0
                            tile.collected = True
                    
                    else:
                        tile.has_dashed = True
                
                tile.update(screen,strawberries)
                tile.fly(screen)
            
            for tile in tiles['moveable']: # Moveable platforms
                
                if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, 30, 30):
                    
                    if self.rect.bottom < tile.rect.centery:
                        
                        if self.vel_y >= 0:
                            self.dy = 0
                            self.rect.bottom = tile.rect.top
                            self.dash = True
                            self.jumped = False
                            self.vel_y = 2
                            self.can_walk = True
                            right_WJs = 0
                            left_WJs = 0 
                            self.coyote_timer = 3
                        
                        if tile.direction == 'Horizontal':
                            self.rect.x += tile.move_direction
                        
                tile.update(tiles, screen)

            # Update sprites colors and reverse
            
            if self.can_walk:
                self.touched_ground += 1
            
            else:
                self.touched_ground = 0

            if self.dash:
                self.sprite = 'red'
            
            if not self.dash:
                self.sprite = 'blue'
            
            if self.reverse:
                self.sprite = 'green'

            if self.flip:
                self.sprite += '_flipped'
                self.flip_left += 1
                self.flip_right = 0
            
            else:
                self.flip_right += 1
                self.flip_left = 0
            
            if self.flip_left == 1 or self.flip_right == 1:
                self.just_flipped = True
            
            else:
                self.just_flipped = False

            self.wj_present = self.all_wj['wall_' + self.sprite]
            self.frames_present = self.all_walking['walk_' + self.sprite]
            self.looking_present = self.all_looking['look_' + self.sprite]

            # Wall slide sprite

            if self.can_WJ:
                screen.blit(self.wj_present, self.rect)

                if self.flip and not self.can_walk and self.stay >= 10: 
                    self.wall_slide_particles.wall_slide(self.rect.bottomleft, (255,255,255), screen)
                
                elif not self.flip and not self.can_walk and self.stay >= 10:
                    self.wall_slide_particles.wall_slide(self.rect.bottomright, (255,255,255), screen)
            
            else:
                
                if self.flip:
                    self.wall_slide_particles.set_position(self.rect.bottomleft[0], self.rect.bottomleft[1] - 5)
                
                else: 
                    self.wall_slide_particles.set_position(self.rect.bottomright[0], self.rect.bottomright[1] - 5)

            # Land on ground particles

            if self.touched_ground <= 20 and self.touched_ground != 0:
                self.land_particles.touched_ground([self.rect.centerx, self.rect.centery + 15], (255,255,255), screen)
            
            else:
                self.land_particles.set_position(self.rect.centerx, self.rect.centery + 15)
                self.land_particles.timer = 0

            # Walking animation

            if not self.is_dashing and not self.is_jumping and self.can_walk and not self.can_WJ and not self.is_WJ:

                if (not down and not up) or left or right:
                    
                    if not left and not right:
                        self.frame_walking = 0
                        self.walking_particles.timer = 0
                        
                        if self.flip:
                            self.walking_particles.set_position(self.rect.bottomright[0], self.rect.bottomright[1])

                        else:
                            self.walking_particles.set_position(self.rect.bottomleft[0], self.rect.bottomleft[1])
                    
                    if self.cooldown <= 0:
                        self.cooldown = 5
                        self.frame_walking += 1 
                    
                        if self.frame_walking == len(self.all_walking['walk_red']):
                            self.frame_walking = 0
                    
                    screen.blit(self.frames_present[self.frame_walking], self.rect)
                    
                    if left or right:
                        
                        if self.just_flipped:
                            self.walking_particles.timer = 0

                            if self.flip:
                                self.walking_particles.set_position(self.rect.bottomright[0], self.rect.bottomright[1])

                            else:
                                self.walking_particles.set_position(self.rect.bottomleft[0], self.rect.bottomleft[1])
                        
                        if self.flip:
                            self.walking_particles.walking(self.rect.bottomright, (255,255,255), screen, True)
                        
                        else:
                            self.walking_particles.walking(self.rect.bottomleft, (255,255,255), screen, False)
            
            else:
                
                if self.flip:
                    self.walking_particles.set_position(self.rect.bottomright[0], self.rect.bottomright[1])

                else:
                    self.walking_particles.set_position(self.rect.bottomleft[0], self.rect.bottomleft[1])

            # Jump and fall sprites
            if not self.can_walk and not self.can_WJ and not self.is_WJ and not self.is_dashing:

                if self.vel_y < 0:
                    screen.blit(self.looking_present[1], self.rect)
                
                if self.vel_y >= 0:
                    
                    if self.vel_y >= 6.5:
                        screen.blit(self.looking_present[0], self.rect)
                    
                    else:
                        screen.blit(self.frames_present[0], self.rect)

            # Check collision with borders

            if self.rect.left + self.dx < 0:
                self.dx = -self.rect.left
            
            if self.rect.right + self.dx > 800:
                self.dx = 800 - self.rect.right
            
            # Check if player fell off the map

            if self.rect.y + self.dy > 810:
                game_over = True
            
            # Update player

            self.rect.x += self.dx
            self.rect.y += self.dy

        # Game over animation

        if game_over:
            color = ['red', 'white']

            self.go_timer += 1

            if self.go_timer == 1:
                self.sfx['death'].play()
                self.death_particle.set_position(self.rect.centerx, self.rect.centery)
            
            if self.go_timer <= 15:
                self.death_particle.death_circles(choice(color), screen)

            if self.go_timer >= 300:
                self.go_timer = 0
                game_over = False
                
        return game_over, strawberries