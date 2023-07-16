import datetime

import pygame
from random import randint
from tetrominos import *
from ui import UIContainer

TILE_SIZE = 30
tetromino_types = ['O', 'L', 'J', 'S', 'Z', 'T', 'I']
class Game:
    def __init__(self, controls, surface_pos, game_type = 'Race'):
        self.grid = None
        self.running = False
        #self.block_lst = []
        self.pre_tetrominos = []
        self.held_tetromino = None
        self.can_hold = True
        self.control_tetromino = None
        self.prepare_next_tetromino = True
        self.width = 10
        self.game_height = 20
        self.buffer = 5

        self.surface_pos = surface_pos

        self.grid_surface = None
        self.grid_pos = (140,0)
        # ui
        self.ui = GameUI(surface_pos, (720, 800), self)

        self.opponents = []

        self.controls = controls

        self.line_counter = 0

        self.start_time = datetime.datetime.now()
        self.time_passed = datetime.datetime.now() - self.start_time

        self.game_type = game_type

        self.start_game(self.width, self.game_height, self.buffer)

    def start_game(self,width, height, buffer):
        self.grid_surface = pygame.Surface((TILE_SIZE*width, TILE_SIZE*(height+buffer)))
        self.grid = GameGrid(self, width, height, buffer, TILE_SIZE)
        # for tetromino in range(0, 5):
        #     random_tetromino = randint(0, 6)
        #     type = tetromino_types[random_tetromino]
        #     self.pre_tetrominos.append(type)
        self.generate_pretetrominos()
        self.start_time = datetime.datetime.now()
        self.running = True

    def create_tetromino(self, spawn_pos, type=''):
        if (type not in tetromino_types):
            random_tetromino = randint(0, 6)
            type = tetromino_types[random_tetromino]
        x=0
        if (type == 'O'):
            self.control_tetromino = TetrominoO(self, (spawn_pos, self.buffer-3), TILE_SIZE)
        if (type == 'L'):
            self.control_tetromino = TetrominoL(self, (spawn_pos, self.buffer-3), TILE_SIZE)
        if (type == 'J'):
            self.control_tetromino = TetrominoJ(self, (spawn_pos, self.buffer-3), TILE_SIZE)
        if (type == 'S'):
            self.control_tetromino = TetrominoS(self, (spawn_pos, self.buffer-3), TILE_SIZE)
        if (type == 'Z'):
            self.control_tetromino = TetrominoZ(self, (spawn_pos, self.buffer-3), TILE_SIZE)
        if (type == 'T'):
            self.control_tetromino = TetrominoT(self, (spawn_pos, self.buffer-3), TILE_SIZE)
        if (type == 'I'):
            self.control_tetromino = TetrominoI(self, (spawn_pos, self.buffer-3), TILE_SIZE)

    def out_of_bounds_block(self):
        print('out of bounds')
        self.running = False

    def generate_pretetrominos(self):
        if (len(self.pre_tetrominos) < 5):
            for tetromino in range(0, 5 - len(self.pre_tetrominos)):
                random_tetromino = randint(0, 6)
                type = tetromino_types[random_tetromino]
                if(len(self.pre_tetrominos) != 0):
                    while (self.pre_tetrominos[len(self.pre_tetrominos) - 1] == type):
                        random_tetromino = randint(0, 6)
                        type = tetromino_types[random_tetromino]
                self.pre_tetrominos.append(type)

    def hold_tetromino(self):
        #first hold
        if(self.held_tetromino is None):
            self.held_tetromino = self.control_tetromino.type
            self.control_tetromino = None
            self.prepare_next_tetromino = True
            # self.create_tetromino(4, self.pre_tetrominos[0])
        #subsequent holds
        else:
            temp_hold = self.control_tetromino.type
            self.create_tetromino(4, self.held_tetromino)
            self.held_tetromino = temp_hold

    def update(self, *args, **kwargs):
        if(self.running==False):
            return
        # self.grid.print_grid()
        #update time
        self.time_passed = datetime.datetime.now() - self.start_time
        if (self.control_tetromino is not None):
            self.control_tetromino.update(args[0], args[1])
            for event in args[1]:
                if event.type == pygame.KEYDOWN:
                    if event.key == self.controls['HOLD'] and self.can_hold == True:
                        self.hold_tetromino()
                        self.can_hold = False
                    if event.key == pygame.K_v:
                        self.grid.garbage_counter += 1
                        print('garbage: ' +str(self.grid.garbage_counter))
                        #self.grid.generate_garbage_row()
        else:
            if(self.prepare_next_tetromino):
                self.create_tetromino(4, self.pre_tetrominos[0])
                self.pre_tetrominos.remove(self.pre_tetrominos[0])
                # if (len(self.pre_tetrominos) < 5):
                #     for tetromino in range(0, 5-len(self.pre_tetrominos)):
                #         random_tetromino = randint(0, 6)
                #         type = tetromino_types[random_tetromino]
                #         while(self.pre_tetrominos[len(self.pre_tetrominos)-1] == type):
                #             random_tetromino = randint(0, 6)
                #             type = tetromino_types[random_tetromino]
                #         self.pre_tetrominos.append(type)
                self.generate_pretetrominos()
                print(self.pre_tetrominos)
                self.prepare_next_tetromino = False
        self.grid.update()

    def draw(self, surface, *args, **kwargs):
        # screen shake
        if(self.grid.screen_shake_time>0):
            self.grid.screen_shake_time -=1
            mag = (int(self.grid.screen_shake_mag[0]),int(self.grid.screen_shake_mag[1]))
            offset = (randint(-mag[0], mag[0]), randint(-mag[1], mag[1]))
            surface.blit(self.grid_surface,
                         (self.surface_pos[0] + offset[0] + self.grid_pos[0],
                          self.surface_pos[1] + offset[1] + self.grid_pos[1]))
        else:
            surface.blit(self.grid_surface,
                         (self.surface_pos[0] + self.grid_pos[0],
                          self.surface_pos[1] + self.grid_pos[1]))
        self.grid_surface.fill(pygame.color.Color('0x000000'))
        self.grid.draw(self.grid_surface)

        if(self.control_tetromino is not None):
            self.control_tetromino.draw(self.grid_surface)

        # for block in self.block_lst:
        #     block.draw(surface)
# FILLED= [(0,24),(1,24),(2,24),(3,24),(4,24),(6,24),(7,24),(6,22)]
# FILLED= [(0,24),(1,24),(2,24),(6,24),(7,24),(6,22),(3,23),(6,23)]
FILLED = []
class GameGrid:
    def __init__(self, game, width, height, buffer, tile_size):
        self.game = game
        self.width = width
        self.height = height + buffer
        # out of bounds area
        self.buffer = buffer

        self.game_height = height
        self.tile_size = tile_size

        # time before row is cleared
        self.clear_row_buffer = 5
        self.clear_row_timer = 0

        # whether to check for filled rows
        self.check_filled_rows = False
        self.filled_rows = []

        # garbage rows
        self.garbage_counter = 0

        self.grid = []
        self.create_grid()

        self.screen_shake_time = 0
        self.screen_shake_mag = (0,0)

        self.tile_shake_time = 0
        self.tile_shake_mag = (0,0)

    def screen_shake(self, duration, mag):
        self.screen_shake_time = duration
        self.screen_shake_mag = mag

    def tile_shake(self, duration, mag):
        self.tile_shake_time = duration
        self.tile_shake_mag = mag

    def create_grid(self):
        for width in range(0, self.width):
            for height in range(0, self.height):
                tile = Tile(self, (width, height), self.tile_size, (height>=self.buffer))
                self.grid.append(tile)
                # print(tile.in_game)
        for x, y in FILLED:
            t = self.get_tile(x,y)
            t.occupied = True
            t.block=GarbageBlock([x,y], self.tile_size)

    def get_tile(self, x, y):
        if(x<0 or y<0):
            #print("index (" + str(x) + "," + str(y) + ") out of bounds")
            return
        index = x * self.height + y
        if(index >= len(self.grid) or index<0):
            #print("index (" + str(x) + "," + str(y) + ") out of bounds")
            return
        return self.grid[index]

    def get_row(self, row_num):
        '''
        Gets the tiles in a single row
        :param row_num: Row number
        :return: List of tiles in row
        '''
        tile_lst = []
        for x_pos in range(0, self.width):
            tile_lst.append(self.get_tile(x_pos, row_num))
        return tile_lst

    def get_filled_rows(self):
        '''
        Gets a list of rows that are filled
        :return: A lst of row numbers
        '''
        row_lst = []
        for row in range(0, self.height):
            occupied = True
            tile_lst = self.get_row(row)
            for tile in tile_lst:
                # print(tile, end=' ')
                if(tile.occupied == False):
                    occupied = False
                    break
            if(occupied != False):
                row_lst.append(row)
        return row_lst

    def clear_row(self, row_num):
        '''
        Removes all blocks in a given row
        :param row_num: Row to be cleared
        :return:
        '''
        for x_pos in range(0, self.width):
            self.get_tile(x_pos, row_num).occupied = False
            self.get_tile(x_pos, row_num).block = None
            self.get_tile(x_pos, row_num).blink = False

    def drop_row(self, row_num):
        '''
        Drops all the blocks in a row down by one row
        :param row_num: Row to be dropped
        :return:
        '''
        #print(row_num)
        for tile in self.get_row(row_num):
            if(tile.block is not None):
                new_tile = self.get_tile(tile.grid_pos[0], tile.grid_pos[1] + 1)
                new_tile.block = tile.block
                new_tile.occupied = True
                tile.block = None
                tile.occupied = False

    def raise_row(self, row_num):
        for tile in self.get_row(row_num):
            if(tile.occupied == True or tile.block is not None):
                above_tile = self.get_tile(tile.grid_pos[0], tile.grid_pos[1] - 1)
                if (above_tile is not None):
                    above_tile.block = tile.block
                    above_tile.occupied = True
                    tile.block = None
                    tile.occupied = False
                else:
                    return

    def generate_garbage_row(self, gap=-1):
        '''
        Generates one row of garbage blocks
        :param gap: The position of the gap. -1 for random, -2 for no gap
        :return:
        '''
        if(gap==-1):
            gap = randint(0, self.game.width-1)
        for row in range(0, self.height):
            self.raise_row(row)
        for tile in range(0, self.width):
            if(tile != gap):
                garbage_block = GarbageBlock([tile, self.height-1], self.tile_size)
                self.get_tile(tile, self.height-1).block = garbage_block
                self.get_tile(tile, self.height-1).occupied = True
        if(self.game.control_tetromino is not None):
            self.game.control_tetromino.update_ghost_blocks()

    def send_rows(self, opponent, rows):
        opponent.grid.garbage_counter += rows

    def update(self, *args, **kwargs):
        # tetromino_active = self.game.control_tetromino is not None
        if(self.screen_shake_time <= 0):
            self.screen_shake_mag = (0, 0)
        if(self.tile_shake_time <= 0):
            self.tile_shake_mag = (0, 0)

        # check for filled rows
        if(self.check_filled_rows == True):
            self.filled_rows = self.get_filled_rows()
            self.check_filled_rows = False
            for row in self.filled_rows:
                for tiles in self.get_row(row):
                    tiles.blink = True
            self.clear_row_timer = self.clear_row_buffer
        #clear filled rows
        rows_cleared = 0
        send_rows = 0
        if(len(self.filled_rows) > 0):
            self.clear_row_timer = self.clear_row_timer - 1
            print(self.clear_row_timer)
            if(self.clear_row_timer <= 0):
                for row in self.filled_rows:
                    self.clear_row(row)
                    rows_cleared = rows_cleared + 1
                    for above in range(row-1,0,-1):
                        self.drop_row(above)
                self.screen_shake(rows_cleared*3+2, (4+3*rows_cleared, 1))
                self.filled_rows = []
            if (self.game.game_type == 'Battle'):
                if (rows_cleared > 0):
                    if (rows_cleared == 4):
                        send_rows = 4
                    elif (rows_cleared != 0):
                        send_rows = (rows_cleared - 1)
                    if (rows_cleared <= 0):
                        send_rows = 0
                if (self.garbage_counter > 0):
                    if (rows_cleared == 4):
                        self.garbage_counter -= 4
                        send_rows -= 4
                    elif (rows_cleared != 0):
                        self.garbage_counter -= (rows_cleared - 1)
                        send_rows -= (rows_cleared - 1)
                self.send_rows(self.game.opponents[0], send_rows)
            if (self.garbage_counter >0 and
                    not self.game.control_tetromino is not None and
                    len(self.filled_rows )==0):
                print(self.garbage_counter)
                for row in range(0,self.garbage_counter,1):
                    self.generate_garbage_row(-1)
                    self.garbage_counter -= 1
                if(self.garbage_counter<=0):
                    self.garbage_counter=0
        # check top
        for x in range(0, self.width,1):
            for y in range(0, self.buffer,1):
                t = self.get_tile(x,y)
                if(t.block is not None and t.in_game==False):
                    print('game over')
                    self.game.running = False
        if(not self.game.control_tetromino is not None and len(self.filled_rows)==0):
            self.game.prepare_next_tetromino = True
        self.game.line_counter += rows_cleared
        if(self.game.line_counter >= 40):
            print('game over')
            self.game.running = False
        # print('grid update')

    def draw(self, surface, *args, **kwargs):
        mag=(0, 0)
        if(self.tile_shake_time>0):
            self.tile_shake_time-=1
            mag=self.tile_shake_mag
        for tile in self.grid:
            tile.draw(surface, mag)

    def print_grid(self):
        for height in range(0, self.height):
            for width in range(0, self.width):
                if(self.get_tile(width, height).occupied == False):
                    print('*', end=' ')
                else:
                    print('x', end=' ')
            print()
        print('\n')

class Tile:
    def __init__(self, grid, grid_pos, size, in_game):
        self.grid = grid
        self.grid_pos = grid_pos
        self.size = size
        self.img = pygame.image.load('./assets/Tile.png')
        self.blink = False
        self.in_game = in_game

        self.block = None
        self.occupied = False

    def __str__(self):
        s = "Tile at " + str(self.grid_pos[0]) + ", " + str(self.grid_pos[1])
        if(self.occupied):
            s = s + ", occupied"
        else:
            s = s + ", empty"
        return s

    def update(self, *args, **kwargs):
        if(self.block is None):
            self.occupied = False
        else:
            self.occupied = True

    def draw(self, surface, shake_mag=(0, 0), *args, **kwargs):
        pos_rect = [self.grid_pos[0] * self.size,
                    self.grid_pos[1] * self.size,
                    self.size,self.size]
        if(not self.in_game and not self.occupied):
            pygame.draw.rect(surface, (25, 25, 25),pos_rect)
        else:
            if(self.occupied):
                if(self.blink == True):
                    surface.blit(self.block.img_lst[1], pos_rect)
                else:
                    surface.blit(self.block.img_lst[0], pos_rect)
            else:
                if (shake_mag[0]>0 or shake_mag[1]>0):
                    offset = (randint(int(-shake_mag[0]),int(shake_mag[0])),
                              randint(int(-shake_mag[1]),int(shake_mag[1])))
                    pos_rect[0] = pos_rect[0] + offset[0]
                    pos_rect[1] = pos_rect[1] + offset[1]
                surface.blit(self.img, pos_rect)

PV_IMGS = {}
for t in tetromino_types:
    PV_IMGS[t] = pygame.image.load('assets/Preveiw Tetrominos/Tetromino' + t +'.png')
class GameUI(UIContainer):
    def __init__(self, pos, size, game):
        super(GameUI, self).__init__(pos, size)
        self.game = game

    def draw(self, surface, *args, **kwargs):
        super().draw(surface)
        pygame.draw.rect(self.surface, (50, 50, 50), (0, 0, 140, 750))

        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, 140, 430))
        pygame.draw.rect(self.surface, (25, 25, 25), (0, 440, 140, 100))
        for tetromino in range(0, len(self.game.pre_tetrominos)):
            pv0_img = PV_IMGS[self.game.pre_tetrominos[tetromino]]
            if(tetromino != 0):
                #pv0_img = pygame.transform.scale(pv0_img, (pv0_img.get_width()*0.5, pv0_img.get_height()*0.5))
                self.surface.blit(pv0_img, (10, tetromino * 80 + 20))
            else:
                self.surface.blit(pv0_img, (10, tetromino + 10))
        if(self.game.held_tetromino is not None):
            hold_img = pygame.image.load('assets/Preveiw Tetrominos/Tetromino' + self.game.held_tetromino + '.png')
            self.surface.blit(hold_img, (10, 450))
        if(self.game.can_hold != True):
            print(self.game.held_tetromino)
            pygame.draw.rect(self.surface, (0, 0, 0), (0, 440, 140, 100))
            if(self.game.held_tetromino != None):
                hold_img = pygame.image.load('assets/Preveiw Tetrominos/Tetromino' + self.game.held_tetromino + '.png')
                self.surface.blit(hold_img, (10, 450))

        line_counter = pygame.font.Font('freesansbold.ttf', 50)
        text = line_counter.render(str(self.game.line_counter), False, (0, 0, 0), (50,50,50))
        self.surface.blit(text, (60, 625))

        #find change in time
        time_diff = self.game.time_passed.total_seconds()
        #format time for output
        min = round(time_diff) // 60
        if(min>=100):
            min=min%100
        sec = round(time_diff) %60
        mil = int((time_diff -int(time_diff)) *100)
        formatted_time = f'{min:02}:{sec:02}:{mil:02}'
        # formatted_time = str(min)+':'+str(sec)+':'+str(mil)

        text = even_spaced_digits(formatted_time, 15, (0,0,0), (50, 50, 50), 'freesansbold.ttf', 25)
        surface.blit(text, (10, 675))
        # timer = pygame.font.Font('freesansbold.ttf', 30)
        # text = timer.render(formatted_time, False, (0, 0, 0), (50, 50, 50))

def even_spaced_digits(text, space, text_color, bg_color, font, font_size):
    text_font = pygame.font.Font(font, font_size)
    surface = pygame.surface.Surface((space*len(text), font_size))
    surface.fill(bg_color)
    for character in range(0, len(text)):
        new_character = text[character]
        text_surface = text_font.render(new_character, False, text_color, bg_color)
        surface.blit(text_surface, ((space * character), 0))
    return surface
