import pygame
from Player import *
from Tile import *
from random import *
from Particles import *

######################################################################

largura = 800
altura = 800
fps = 60
player = Player(50, 200)
ground = pygame.Rect(0, 620, 720, 40)
rodar = True

pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()

def desenhar_matriz(tela, linhas, colunas, largura, altura):
    # Calcula o tamanho de cada célula
    cell_width = largura // colunas
    cell_height = altura // linhas

    for linha in range(linhas):
        for coluna in range(colunas):
            # Calcula as coordenadas da célula
            x = coluna * cell_width
            y = linha * cell_height
            # Desenha o retângulo na tela
            pygame.draw.rect(tela, (255, 255, 0), pygame.Rect(x, y, cell_width, cell_height), 2)

fase = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 20, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 19, 17, 0, 18, 1, 16, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 17, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

tiles = Tile(fase)
background = pygame.image.load('assets/maps/level 1.png')
fundo = pygame.transform.scale(background, (800, 800))
fundo_rect = fundo.get_rect()
fundo_rect = pygame.Rect(0, 0, 45, 45)
game_over = False
strawberries = 0
shake = [0,0]
shake_timer = 0
snow = Particles(0, 0, 80)
snow.random_position([0,800], [0,800])
time = 0
hours = 0
minutes = 0
total_time = f'{hours}:{minutes}:{time}'
pygame.time.set_timer(pygame.USEREVENT, 1000)
while rodar:
    
    #print(player.vel_y)
    total_time = f'{hours}:{minutes}:{time}'
    print(total_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
        if event.type == pygame.USEREVENT:
            time += 1
    tela.blit(fundo, fundo_rect)
    #desenhar_matriz(tela, 20, 20, largura, altura)
    if game_over:
        game_over,strawberries = player.controls(tiles.tiles_dict, tela, game_over,strawberries)
        clock.tick(fps)
        tiles.draw(tela)
        pygame.display.update()
        if not game_over:
            player.rect.x = largura/2
            player.rect.y = altura/2
    else: 
        game_over,strawberries = player.controls(tiles.tiles_dict, tela, game_over,strawberries)
        
        if player.screen_shake and player.is_dashing:
            shake_timer += 1
            shake[0] = randint(-4,4)
            shake[1] = randint(-4,4)

            if shake_timer >= 14 or not player.is_dashing:
                player.screen_shake = False
                shake = [0, 0]
                shake_timer = 0


        elif player.screen_shake:
            shake_timer += 1
            shake[0] = randint(-2,2)
            shake[0] = randint(-2,2)

            if shake_timer >= 10:
                player.screen_shake = False
                shake = [0, 0]
                shake_timer = 0
            
        clock.tick(fps)
        tiles.draw(tela)
        snow.snowing('white', screen, [-5, 7])
        tela.blit(pygame.transform.scale(tela,(800,800)), shake)


        if time == 60:
            time = 0 
            minutes += 1
            change = True
            if minutes == 60:
                minutes = 0
                hours += 1

        pygame.display.update()
    
pygame.quit()