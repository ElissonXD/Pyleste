import pygame
from random import *

# Particles class

class Particles:
    def __init__(self, x, y, value):
        self.particles = []

        for particle in range(value):
            self.particles.append(pygame.Rect(x, y, 2, 2))
        
        self.x = x
        self.y = y

        # Circle rect for explosion effect
        self.circle_rect = pygame.Rect(x, y, 2, 2)

        # Timer for some particles
        self.timer = 0

    # Shaking
    def shaking_particles(self, color, screen):
        
        for particle in self.particles:
            particle.y += randint(1,4)

            if particle.y > self.y + randint(25,50):
                particle.y = self.y 
                particle.x = self.x + randint(0,40)
        
            pygame.draw.rect(screen, color, particle, 2, 2)

    # Explosion 
    def explosion_particles(self, color, screen):
            
        for particle in self.particles:
            particle.x += randint(-30,30)
            particle.y += randint(-30,30)
            pygame.draw.rect(screen, color, particle, 2, 2)
    
    def circle_explosion(self, screen, color):
        
        self.circle_rect.width += 50
        self.circle_rect.height += 50
        self.circle_rect.y  -= 25
        self.circle_rect.x -= 25
        pygame.draw.arc(screen, color, self.circle_rect, 0, 6.28, 1)
    
    def circle_reverse(self,screen, color):
        
        self.circle_rect.width -= 50
        self.circle_rect.height -= 50
        self.circle_rect.y  += 25
        self.circle_rect.x += 25
        pygame.draw.arc(screen, color, self.circle_rect, 0, 6.28, 1)
    
    # Dash 
    def dash(self, p_gravity, p_x, color, screen):

        if p_gravity < 0:

            for particle in self.particles:
                particle.y += randint(0,15)
                particle.x += randint(-3,3)

        if p_gravity > 0:
        
            for particle in self.particles:
                particle.y += randint(-15,0)
                particle.x += randint(-3,3)
        
        if p_x > 0:

            for particle in self.particles:
                particle.y += randint(0,3)
                particle.x += randint(-15,0)
        
        if p_x < 0:

            for particle in self.particles:
                particle.y += randint(0,3)
                particle.x += randint(0,15)
        
        for particle in self.particles:
            pygame.draw.rect(screen, color, particle, 2, 2)

    # Wall slide
    def wall_slide(self, p_pos, color, screen):
        
        for particle in self.particles:
            particle.y -= randint(1,10)
            particle.x += randint(-2,2)

            if particle.y < p_pos[1] - randint(50,100):
                particle.y = p_pos[1] - 5
                particle.x = p_pos[0]
            
            pygame.draw.rect(screen, color, particle, 2, 2)

    # Walking
    def walking(self, p_pos, color, screen, flip):
        self.timer += 1

        for particle in self.particles:

            if flip:
                particle.x += randint(2,8)
            
            else:
                particle.x -= randint(2,8)
            
            if self.timer <= 10:
                particle.y -= randint(2,5)
            
            if self.timer >= 10:
                particle.y += randint(2,5)

            pygame.draw.rect(screen, color, particle, 2, 2)

        if self.timer >= 15:
            self.timer = 0

            for particle in self.particles:
                particle.x = p_pos[0]
                particle.y = p_pos[1]

    # Land
    def touched_ground(self, p_pos, color, screen):
        self.timer += 1

        for particle, multiplier in zip(self.particles, range(len(self.particles))):

            if multiplier % 2 == 0:
                particle.x -= randint(5,10)

                if self.timer == 1:
                    particle.x -= 5 * multiplier
            
            else:
                particle.x += randint(5,10)

                if self.timer == 1:
                    particle.x += 5 * multiplier
            
            if self.timer <= 10:
                particle.y -= randint(2,4)
            
            else:
                particle.y += randint(2,4)

            pygame.draw.rect(screen, color, particle, 2, 2)

        if self.timer >= 20:
            self.timer = 0

            for particle in self.particles:
                particle.x = p_pos[0]
                particle.y = p_pos[1]

    # Death
    def death_circles(self, color, screen):

        self.particles[0].y -= 10
        self.particles[1].y += 10
        
        self.particles[2].x += 10
        self.particles[2].y -= 10
        self.particles[3].x -= 10
        self.particles[3].y -= 10

        self.particles[4].x += 10
        self.particles[5].x -= 10

        self.particles[6].x += 10
        self.particles[6].y += 10
        self.particles[7].x -= 10
        self.particles[7].y += 10

        for particle in self.particles:
            pygame.draw.circle(screen, color, particle.center, 20, 20)

    # Snowing
    def snowing(self, color, screen, speed):

        for particle in self.particles:
            particle.y += speed[1]
            particle.x += speed[0]

            pygame.draw.circle(screen, color, particle.center, 3, 3)

            if particle.y > 850 or particle.x < -300:
                particle.y = -10
                particle.x = randint(-200,1300)

    # Add gravity
    def add_gravity(self, gravity, color, screen):

        for particle in self.particles:
            particle.y += gravity
            pygame.draw.rect(screen, color, particle, 2, 2)

    # Set to another postion
    def set_position(self, x, y):

        for particle in self.particles:
            particle.x = x
            particle.y = y

    # Set particles to random positions
    def random_position(self, posx, posy):

        for particle in self.particles:
            particle.x += randint(posx[0], posx[1])
            particle.y += randint(posy[0], posy[1])
        
    # Return to initial postion 
    def initial_position(self):

        for particle in self.particles:
            particle.x = self.x
            particle.y = self.y
        
        self.circle_rect = pygame.Rect(self.x, self.y, 2, 2)
        self.timer = 0
    
    # Draw particles
    def draw_particles(self,screen,color):
        
        for particle in self.particles:
            pygame.draw.rect(screen, color, particle, 2, 2)