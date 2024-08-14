import pygame

class Player:
    global gravity, left_dash, right_dash, up_dash, down_dash
    gravity = 1
    left_dash = False
    right_dash = False
    up_dash = False
    down_dash = False

    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        self.jump = 20
        self.jump_timer = 0
        self.jumped = False
        self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.dx = 0
        self.dy = 0
        self.dash_speed = 15
        self.dash_time = 10
        self.vel_y = 0
        self.dash = True
        self.is_dashing = False
        self.dash_timer = 0


    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0) ,self.rect)

    def controls(self, ground):
        
        global gravity, left_dash, right_dash, down_dash, up_dash
        self.dx = 0
        self.dy = 0
        down = False
        left = False
        right = False
        up = False

        # Controls

        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT] and not left_dash:
            self.dx -= 10 
            left = True
        if key[pygame.K_d] or key[pygame.K_RIGHT] and not right_dash:
            self.dx += 10
            right = True 
        if (key[pygame.K_w] or key[pygame.K_UP]) and not self.jumped:
            self.vel_y -= self.jump
            self.jumped = True
            self.is_jumping = True
            up = True
        if key[pygame.K_s] or key[pygame.K_DOWN] and self.vel_y != 0:
            down = True
        
        
        # Jump

        if self.is_jumping:
            self.jump_timer += 1
            if self.jump_timer >= 10:
                self.is_jumping= False
                self.jump_timer = 0

        # Dash

        if key[pygame.K_SPACE] and self.dash and not self.is_dashing:
            self.is_dashing = True
            self.dash = False
            self.is_jumping = False
            self.jumped = True
            if left:
                self.dx = -self.dash_speed
                left_dash = True
            if right:
                self.dx = self.dash_speed
                right_dash = True
            if down:
                self.vel_y = self.dash_speed
                down_dash = True
            if key[pygame.K_w] or key[pygame.K_UP]:
                self.vel_y = -self.dash_speed
                up_dash = True
            if not left and not up and not right and not down:
                self.vel_y = -self.dash_speed
                up_dash = True

            
        if self.is_dashing:
            self.dash_timer += 1
            if left_dash:
                self.dx = -self.dash_speed 
                if not up_dash and not down_dash:
                    self.vel_y = 0
            if right_dash:
                self.dx = self.dash_speed 
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

        if not self.is_dashing and not self.is_jumping:
            self.vel_y += gravity
            if down: 
                self.vel_y = 10
            else:
                if self.vel_y >= 5:
                    self.vel_y = 5
        
        self.dy += self.vel_y

        # Colision with ground

        if ground.colliderect(self.rect.x, self.rect.y + self.dy, 30, 30) and self.vel_y > 0:
            if self.rect.bottom < ground.centery:
                if self.vel_y >= 0: 
                    self.rect.bottom = ground.top
                    self.dy = 0
                    self.dash = True
                    self.jumped = False
            else:
                self.jumped = True
        else:
            self.jumped = True
            

        # Colision with special things(work later)

        # Update player

        self.rect.x += self.dx
        self.rect.y += self.dy   