import pygame
from game import Game

run=True

pygame.init()
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

BG_COLOR = pygame.color.Color('0x505050')

game = Game()
i=0
while (run):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    game.update(pygame.key.get_pressed(), events)
    # print(game.grid.get_tile(100,8))
    #_____Draw_____
    window.fill(BG_COLOR)
    game.draw(window)

    pygame.display.flip()
    # print(i)
    i= i+1
    clock.tick(FPS)
