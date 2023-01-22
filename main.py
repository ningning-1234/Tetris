import pygame
from game import Game

run=True

pygame.init()
pygame.font.init()

WIN_WIDTH = 400
WIN_HEIGHT = 625
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

BG_COLOR = pygame.color.Color('0x505050')

game = Game()

while (run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    game.update()
    # print(game.grid.get_tile(100,8))
    #_____Draw_____
    window.fill(BG_COLOR)
    game.draw(window)

    pygame.display.flip()
    clock.tick(FPS)
