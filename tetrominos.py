import pygame.image


class Tetromino:
    def __init__(self, game, start_pos, type, img, size):
        self.game = game
        self.type = type
        self.img = img
        self.size = size
        self.blocks = []
        self.create_blocks(start_pos)
        self.rotation = 0
        self.falling = True
        self.fall_delay = 30
        self.last_fall = 0

    def create_blocks(self, start_pos):
        pass

    def move(self, dir):
        pass

    def fall(self):
        for block in self.blocks:
            block.fall()

    def rotate(self):
        pass

    def stop_fall(self):
        '''
        when the tetromino can no longer fall
        :return:
        '''
        print('stopped falling')

    def update(self, *args, **kwargs):
        for block in self.blocks:
            if(block.can_fall() == False):
                self.falling = False
        if(self.falling == True):
            self.last_fall = self.last_fall + 1
            if(self.last_fall >= self.fall_delay):
                self.fall()
                self.last_fall = 0
        else:
            self.stop_fall()

    def draw(self, surface, *args, **kwargs):
        for block in self.blocks:
            block.draw(surface)

class TetrominoBlock:
    def __init__(self, tetromino, grid_pos, size):
        self.tetromino = tetromino
        self.img = self.tetromino.img
        self.grid_pos = grid_pos
        self.size = size

    def fall(self):
        self.grid_pos[1] = self.grid_pos[1] + 1

    def can_fall(self):
        if(self.grid_pos[1] + 1 >= self.tetromino.game.grid.height):
            return False
        return True

    def update(self, *args, **kwargs):
        pass

    def draw(self, surface, *args, **kwargs):
        surface.blit(self.img, (self.grid_pos[0] * self.size, self.grid_pos[1] * self.size))

O_IMG = pygame.image.load('assets/TetrominoO.png')
class TetrominoO(Tetromino):
    def __init__(self, game, start_pos,  size):
        super().__init__(game, start_pos, 'O', O_IMG, size)

    def create_blocks(self, start_pos):
        # todo
        #  make sure tetromino cannot have blocks outside of the grid
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)

class TetrominoL(Tetromino):
    pass

class TetrominoJ(Tetromino):
    pass

class TetrominoS(Tetromino):
    pass

class TetrominoZ(Tetromino):
    pass

class TetrominoT(Tetromino):
    pass

class TetrominoI(Tetromino):
    pass
