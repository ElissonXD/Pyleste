import pygame

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

    def __init__(self, x, y):
        
        # Coordenates and rect
        img = pygame.image.load('classes/ichiban.png')
        self.img = pygame.transform.scale(img, (30,30))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = 0
        self.vel_y = 0
        self.go_timer = 0

        # Stick
        self.sticked = False
        self.sideways_stick = False
        
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
        self.tramp_height = -15
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

    def controls(self, tiles, screen, game_over, strawberries):
        
        global gravity, left_dash, right_dash, down_dash, up_dash, right_WJs, left_WJs
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
                    self.dx -= 5
                    left = True 
            
            if key[pygame.K_RIGHT] and not self.is_dashing and not self.is_WJ:
                
                if self.reverse_timer > 0 and left_dash:
                    self.reverse_timer -= 1
                
                else:
                    self.dx += 5
                    right = True 
            
            if key[pygame.K_UP]:
                up = True
            
            if key[pygame.K_x] and not self.jumped:
                self.vel_y = -self.jump
                self.jumped = True
                self.is_jumping = True
                self.sticked = False
            
            if key[pygame.K_DOWN]:
                self.sticked = False
                down = True
            
            # Jump Logic

            if self.is_jumping:
                self.jump_timer += 1
                
                if self.jump_timer >= 15:
                    self.is_jumping= False
                    self.jump_timer = 0

            # Is Wall Jumping

            if self.is_WJ:
                self.WJ_timer += 1
                
                if self.right_WJ:
                    self.dx = -5 
                    
                    if right_WJs == 1:
                        self.vel_y = -self.WJ_height
                    
                    else:
                        self.vel_y = -3
                
                elif self.left_WJ:
                    self.dx = 5
                    
                    if left_WJs == 1:
                        self.vel_y = -self.WJ_height
                    
                    else:
                        self.vel_y = -3             
                
                if self.WJ_timer >= 15:
                    self.WJ_timer = 0
                    self.is_WJ = False
                    self.right_WJ = False
                    self.left_WJ = False

            # Dash Logic

            if key[pygame.K_c] and self.dash and not self.is_dashing:
                self.is_dashing = True
                self.dash = False
                self.is_jumping = False
                self.jump_timer = 0
                self.jumped = True
                self.is_WJ = False
                self.sticked = False
                self.WJ_timer = 0
                
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
                
                if self.dash_timer >= 15:
                    self.is_dashing = False
                    self.dash_timer = 0
                    left_dash = False
                    right_dash = False
                    up_dash = False
                    down_dash = False

            # Gravity

            if not self.is_dashing and not self.is_jumping and not self.can_WJ and not self.is_WJ and not self.sticked:
                self.vel_y += gravity
                if self.reverse_timer > 0:
                    self.reverse_timer -= 1 
                else: 
                    if down: 
                        self.vel_y = 9
                    
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
                            self.jumped = False
                            right_WJs = 0
                            left_WJs = 0 
                            self.coyote_timer = 3

            for tile in tiles['green']: # Green Crystals
                
                if tile.data[2]:
                    
                    if tile.data[0].colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30) and not self.dash:
                        self.dash = True
                        tile.data[2] = False
                
                tile.update(screen)

            for tile in tiles['red']: # Red Crystals
                
                if tile.data[2]:
                    
                    if tile.data[0].colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30) and not self.dash:
                        self.reverse = True
                        self.dash = True
                        tile.data[2] = False
                
                tile.update(screen)

            for tile in tiles['trampoline']: # Trampoline
                
                # Y direction

                if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, 30, 30):
                    self.vel_y = self.tramp_height
                    self.dash = True
                    self.jumped = True
                    self.is_jumping = True
                
                # X direction

                if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y, 30, 30):
                    self.vel_y = self.tramp_height
                    self.dash = True
                    self.jumped = True
                    self.is_jumping = True
            
                tile.draw()

            for tile in tiles['spike']: # Spikes
                
                if tile.colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30):
                    game_over = True

            for tile in tiles['block']: # Blocks
                
                if tile.data[4] <= 30:

                    # X direction
                    
                    if tile.data[0].colliderect(self.rect.x + self.dx, self.rect.y, 30, 30):
                        self.dx = 0
                        tile.data[3] = False

                        # Wall Jump Logic
                        
                        self.is_WJ = False
                        self.WJ_timer = 0

                        # Wall Jump Logic
                        if right and self.vel_y > 0:
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
                        
                        elif left and self.vel_y > 0:
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
                            tile.data[3] = False
                            self.dy = tile.data[0].bottom - self.rect.top
                            self.is_dashing = False
                            self.is_jumping = False
                            self.dash_timer = 0
                            self.jump_timer = 0
                            self.is_WJ = False
                            self.WJ_timer = 0
                            self.vel_y = 0
                        
                        elif self.vel_y >= 0:
                            tile.data[3] = False
                            self.dy = tile.data[0].top - self.rect.bottom
                            self.dash = True
                            self.jumped = False
                            right_WJs = 0
                            left_WJs = 0 
                            self.coyote_timer = 3
            
                tile.update(screen)

            for tile in tiles['strawberry']:  # Strawberry
                
                if not tile.bolean:
                    
                    if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y + self.dy, 30, 30):
                        tile.bolean = True
                        tile.display_straw = True
                        strawberries += 1
                
                tile.update(screen,strawberries)
            
            for tile in tiles['sticky']:  # Sticky
                
                # X direction

                if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y, 30, 30):
                    self.sticked = True
                    self.dx = 0
                    self.dy = 0
                    self.vel_y = 0
                    self.sideways_stick = True

                # Y direction

                if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, 30, 30):
                    self.sticked = True
                    self.dx = 0
                    self.dy = 0
                    self.sideways_stick = False
                    
                    if self.vel_y < 0:
                        self.dy = tile.rect.bottom - self.rect.top
                        self.is_dashing = False
                        self.is_jumping = False
                        self.dash_timer = 0
                        self.jump_timer = 0
                        self.is_WJ = False
                        self.WJ_timer = 0
                        self.vel_y = 0
                    
                    elif self.vel_y >= 0:
                        self.dy = tile.rect.top - self.rect.bottom
                        self.dash = True
                        self.jumped = False
                        right_WJs = 0
                        left_WJs = 0 
                        self.coyote_timer = 3
                        self.vel_y = 5
                
                tile.draw(screen)
            
            for tile in tiles['moveable']: # Moveable platforms
                
                if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, 30, 30):
                    
                    if self.rect.bottom < tile.rect.centery:
                        
                        if self.vel_y >= 0:
                            self.dy = 0
                            self.rect.bottom = tile.rect.top
                            self.dash = True
                            self.jumped = False
                            right_WJs = 0
                            left_WJs = 0 
                            self.coyote_timer = 3
                        
                        if tile.direction == 'Horizontal':
                            self.rect.x += tile.move_direction
                        
                tile.update(screen)

            # Sticky logic

            if self.sticked:
                self.dx = 0
                self.dy = 0
                
                if self.sideways_stick:
                    
                    if left:
                        self.can_WJ = True
                        
                        if key[pygame.K_x] and not self.is_WJ:
                            self.is_WJ = True
                            self.right_WJ = True
                            self.jumped = True
                            right_WJs += 1
                            left_WJs = 0
                            self.sticked = False
                    
                    elif right:
                        self.can_WJ = True
                        
                        if key[pygame.K_x] and not self.is_WJ:
                            self.is_WJ = True
                            self.left_WJ = True
                            self.jumped = True
                            right_WJs = 0
                            left_WJs += 1
                            self.sticked = False 


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

            screen.blit(self.img, self.rect)

        if game_over:
            # Change later
            go_img = pygame.image.load('assets/sprites/kiryu.png')
            go_img2 = pygame.transform.scale(go_img, (30,30))
            screen.blit(go_img2, self.rect)
            self.go_timer += 1
           
            if self.go_timer >= 300:
                self.go_timer = 0
                game_over = False
                
        return game_over, strawberries
