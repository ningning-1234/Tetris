import pygame
from game import Game

# todo
#  add effect when tetromino stops moving
#  add effect when 2 or more rows are cleared
#  improve push accuracy
#  add x and y magnitude to shaking
#  do not queue more than two of the same tetrominos
run=True

pygame.init()
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

BG_COLOR = pygame.color.Color('0x505070')

game = Game((0,20))
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
