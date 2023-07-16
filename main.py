import pygame
from game import Game
from ui import UI_MANAGER

run=True

pygame.init()
pygame.font.init()

WIN_WIDTH = 880
WIN_HEIGHT = 750
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

BG_COLOR = pygame.color.Color('0x303030')

game1_controls = {'LEFT': pygame.K_LEFT,
                  'RIGHT': pygame.K_RIGHT,
                  'SOFT DROP': pygame.K_DOWN,
                  'HARD DROP': pygame.K_UP,
                  'ROTATE LEFT': pygame.K_COMMA,
                  'ROTATE RIGHT': pygame.K_PERIOD,
                  'HOLD': pygame.K_SLASH}

game2_controls = {'LEFT': pygame.K_a,
                  'RIGHT': pygame.K_d,
                  'SOFT DROP': pygame.K_s,
                  'HARD DROP': pygame.K_w,
                  'ROTATE LEFT': pygame.K_b,
                  'ROTATE RIGHT': pygame.K_n,
                  'HOLD': pygame.K_m}

game1 = Game(game1_controls, (0,0))
game2 = Game(game2_controls, (440,0))

game1.opponents.append(game2)
game2.opponents.append(game1)
# game2 = Game((300,0))
ui = UI_MANAGER
i=0
while (run):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    game1.update(pygame.key.get_pressed(), events)
    game2.update(pygame.key.get_pressed(), events)
    # print(game.grid.get_tile(100,8))
    #_____Draw_____
    window.fill(BG_COLOR)
    game1.draw(window)
    game2.draw(window)
    ui.draw(window)

    pygame.display.flip()
    # print(i)
    i= i+1
    clock.tick(FPS)
