import pygame
from tetrominos import *

TILE_SIZE = 30
class Game:
    def __init__(self):
        self.grid = None
        self.running = False
        self.block_lst = []
        self.control_tetromino = None

        self.start_game(10,20)

    def start_game(self,width, height):
        self.grid_surface = pygame.Surface((TILE_SIZE*width, TILE_SIZE*height))
        self.grid = GameGrid(self, width, height, TILE_SIZE)
        self.create_tetromino()
        self.running = True

    def create_tetromino(self, type='R'):
        # todo
        #  create the tetromino based on type
        #  type R means random
        self.control_tetromino = TetrominoO(self, (-1,0), TILE_SIZE)

    def update(self, *args, **kwargs):
        self.control_tetromino.update()

    def draw(self, surface, *args, **kwargs):
        surface.blit(self.grid_surface, (0, 0))
        self.grid.draw(self.grid_surface)
        if(self.control_tetromino is not None):
            self.control_tetromino.draw(surface)
        for block in self.block_lst:
            block.draw(surface)

class GameGrid:
    def __init__(self, game, width, height, tile_size):
        self.game = game
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid = []
        self.create_grid()

    def create_grid(self):
        for width in range(0, self.width):
            for height in range(0, self.height):
                tile = Tile(self, (width, height), self.tile_size)
                self.grid.append(tile)

    def get_tile(self, x, y):
        index = x * self.height + y
        if(index > len(self.grid) or index<0):
            print("index (" + str(x) + "," + str(y) + ") out of bounds")
            return
        return self.grid[index]

    def update(self, *args, **kwargs):
        pass

    def draw(self, surface, *args, **kwargs):
        for tile in self.grid:
            tile.draw(surface, (0, 0, 0))

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
