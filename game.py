import pygame
from random import randint
from tetrominos import *

TILE_SIZE = 30
class Game:
    def __init__(self):
        self.grid = None
        self.running = False
        #self.block_lst = []
        self.control_tetromino = None

        self.start_game(10,20)

    def start_game(self,width, height):
        self.grid_surface = pygame.Surface((TILE_SIZE*width, TILE_SIZE*height+200))
        self.grid = GameGrid(self, width, height, TILE_SIZE)
        self.create_tetromino(4,'I')
        self.running = True

    def create_tetromino(self, spawn_pos, type='I'):
        tetromino_types = ['O', 'L', 'J', 'S', 'Z', 'T', 'I']
        if (type not in tetromino_types):
            random_tetromino = randint(0, 6)
            type = tetromino_types[random_tetromino]
        x=0
        if (type == 'O'):
            self.control_tetromino = TetrominoO(self, (spawn_pos, -2+x), TILE_SIZE)
        if (type == 'L'):
            self.control_tetromino = TetrominoL(self, (spawn_pos, -3+x), TILE_SIZE)
        if (type == 'J'):
            self.control_tetromino = TetrominoJ(self, (spawn_pos, -3+x), TILE_SIZE)
        if (type == 'S'):
            self.control_tetromino = TetrominoS(self, (spawn_pos, -2+x), TILE_SIZE)
        if (type == 'Z'):
            self.control_tetromino = TetrominoZ(self, (spawn_pos, -2+x), TILE_SIZE)
        if (type == 'T'):
            self.control_tetromino = TetrominoT(self, (spawn_pos, -2+x), TILE_SIZE)
        if (type == 'I'):
            self.control_tetromino = TetrominoI(self, (spawn_pos, -4+x), TILE_SIZE)

    def out_of_bounds_block(self):
        print('game over')
        self.running = False

    def update(self, *args, **kwargs):
        if(self.running==False):
            return
        # self.grid.print_grid()
        if (self.control_tetromino is not None):
            self.control_tetromino.update(args[0], args[1])
        else:
            self.create_tetromino(4,'I')
        self.grid.update()

    def draw(self, surface, *args, **kwargs):
        surface.blit(self.grid_surface, (0, 200))
        self.grid.draw(self.grid_surface)
        if(self.control_tetromino is not None):
            self.control_tetromino.draw(surface)
        # for block in self.block_lst:
        #     block.draw(surface)

class GameGrid:
    def __init__(self, game, width, height, tile_size):
        self.game = game
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.check_filled_rows = False
        self.grid = []
        self.create_grid()

    def create_grid(self):
        for width in range(0, self.width):
            for height in range(0, self.height):
                tile = Tile(self, (width, height), self.tile_size)
                self.grid.append(tile)

    def get_tile(self, x, y):
        if(x<0 or y<0):
            print("index (" + str(x) + "," + str(y) + ") out of bounds")
            return
        index = x * self.height + y
        if(index > len(self.grid) or index<0):
            print("index (" + str(x) + "," + str(y) + ") out of bounds")
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
            print(occupied)
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

    def drop_row(self, row_num, drops=1):
        '''
        Drops all the blocks in a row down by a given amount
        :param row_num: Row to be dropped
        :param drops: Number of rows to drop
        :return:
        '''
        # todo
        #  drop rows
        pass

    def update(self, *args, **kwargs):
        if(self.check_filled_rows==True):
            self.check_filled_rows = False
            for row in self.get_filled_rows():
                self.clear_row(row)
        # print('grid update')
        #todo
        # check for filled rows and print the row number
        # clear the rows
        # drop the blocks above

    def draw(self, surface, *args, **kwargs):
        for tile in self.grid:
            tile.draw(surface, (0, 0, 0))

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
    def __init__(self, grid, grid_pos, size):
        self.grid = grid
        self.grid_pos = grid_pos
        self.size = size
        self.img = pygame.image.load('./assets/Tile.png')

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

    def draw(self, surface, *args, **kwargs):
        surface.blit(self.img, (self.grid_pos[0]*self.size, self.grid_pos[1]*self.size))
        if(self.occupied != False):
            surface.blit(self.block.img, (self.grid_pos[0] * self.size, self.grid_pos[1] * self.size))
