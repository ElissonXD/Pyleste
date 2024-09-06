import pygame
from Player import *
from Tile import *

######################################################################

largura = 800
altura = 800
fps = 60
player = Player(largura/2, altura/2)
ground = pygame.Rect(0, 620, 720, 40)
rodar = True

pygame.init()
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
    [4, 1, 1, 1, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 5],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0, 0, 5],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0, 0, 5],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0, 0, 5],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 15, 0, 0, 0, 15, 0, 0, 0, 5],
    [4, 2, 2, 2, 2, 7, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 5],
    [4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 12, 0, 0, 0, 0, 0, 1, 1, 1],
    [4, 3, 3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0],
    [4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 14, 14, 0, 0, 0, 0, 0],
    [4, 0, 18, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1, 1, 1],
    [4, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 5],
    [4, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 5],
    [4, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [4, 0, 0, 5, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [4, 0, 18, 0, 0, 0, 0, 0, 0, 10, 16, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [4, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

tiles = Tile(fase)
background = pygame.image.load('assets/maps/test_map.png')
fundo = pygame.transform.scale(background, (800, 800))
fundo_rect = fundo.get_rect()
fundo_rect = pygame.Rect(0, 0, 45, 45)
game_over = False
strawberries = 0


while rodar:
    
    print(player.vel_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
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

        clock.tick(fps)
        tiles.draw(tela)

        pygame.display.update()
    
pygame.quit()
