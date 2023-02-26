import pygame.image


class Tetromino:
    def __init__(self, game, start_pos, type, img, size):
        self.game = game
        self.type = type
        self.img = img
        self.size = size
        self.blocks = []
        self.pivot = None
        self.create_blocks(start_pos)
        self.rotation = 0
        self.falling = True

        # self.fall_delay = 15
        self.fall_delay = 100000
        self.last_fall = 0

        self.move_delay = 5
        self.last_move = self.move_delay

        self.soft_drop_delay = 5
        self.last_soft_drop = self.soft_drop_delay


    def create_blocks(self, start_pos):
        pass

    def move(self, dir):
        if (self.check_move(dir) == True):
            for block in self.blocks:
                block.grid_pos[0] = block.grid_pos[0] + dir
            self.last_move = 0

    def soft_drop(self):
        self.fall()
        self.last_soft_drop = 0

    def hard_drop(self):
        for block in self.blocks:
            block.grid_pos[1] = block.grid_pos[1] + 15
        self.last_soft_drop = 0

    def fall(self):
        for block in self.blocks:
            block.fall()

    def find_landing_spot(self):

        return 0

    def rotate(self, dir):
        '''
        Rotates the tetromino
        :param dir:
        1 = Clockwise
        -1 = Counter clockwise
        :return:
        '''
        if(dir==1):
            print('rotate clockwise')
        else:
            print('rotate counterclockwise')

    def hard_drop(self):
        while(self.can_fall()):
            self.fall()
        self.stop_fall()

    def can_fall(self):
        for block in self.blocks:
            if (block.can_fall() == False):
                return False
        return True

    def stop_fall(self):
        '''
        when the tetromino can no longer fall
        :return:
        '''
        # self.game.block_lst = self.game.block_lst + self.blocks
        for block in self.blocks:
            tile = self.game.grid.get_tile(block.grid_pos[0], block.grid_pos[1])
            if(tile is not None):
                self.game.block_lst.append(block)
                tile.block = block
                tile.occupied = True
            else:
                self.game.out_of_bounds_block()
        self.game.control_tetromino = None

    def check_move(self, dir):
        for block in self.blocks:
            if (block.grid_pos[0] + dir > self.game.grid.width - 1 or block.grid_pos[0] + dir < 0):
                return False
            if (self.game.grid.get_tile(block.grid_pos[0] + dir, block.grid_pos[1]) is not None):
                if (self.game.grid.get_tile(block.grid_pos[0] + dir, block.grid_pos[1]).occupied == True):
                    return False
        return True

    def update(self, *args, **kwargs):
        for block in self.blocks:
            block.update()
        if (args[0][pygame.K_LEFT] == True and self.last_move >= self.move_delay):
            # if (args[0][pygame.K_DOWN] == True and self.last_soft_drop >= self.soft_drop_delay):
            #     self.soft_drop()
            self.move(-1)
        if (args[0][pygame.K_RIGHT] == True and self.last_move >= self.move_delay):
            # if (args[0][pygame.K_DOWN] == True and self.last_soft_drop >= self.soft_drop_delay):
            #     self.soft_drop()
            self.move(1)

        self.last_soft_drop = self.last_soft_drop + 1
        self.last_move = self.last_move + 1
        for event in args[1]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.rotate(-1)
                if event.key == pygame.K_x:
                    self.rotate(1)

        if (self.falling == True):
            if (self.can_fall() == False):
                self.falling = False
                self.stop_fall()
                return
            self.last_fall = self.last_fall + 1
            if (args[0][pygame.K_DOWN] == True and self.last_soft_drop >= self.soft_drop_delay):
                self.soft_drop()
                self.last_fall = 0
            elif(self.last_fall >= self.fall_delay):
                self.fall()
                self.last_fall = 0
        for event in args[1]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.hard_drop()
                    return

    def draw(self, surface, *args, **kwargs):
        for block in self.blocks:
            block.draw(surface)

class TetrominoBlock:
    def __init__(self, tetromino, grid_pos, size):
        self.tetromino = tetromino
        self.img = self.tetromino.img
        self.grid_pos = grid_pos
        self.next_pos = self.grid_pos.copy()
        self.size = size

    def fall(self):
        self.grid_pos[1] = self.grid_pos[1] + 1

    def can_fall(self):
        if (self.grid_pos[1] + 1 >= self.tetromino.game.grid.height):
            return False
        for block in self.tetromino.game.block_lst:
            if (self.grid_pos[0] == block.grid_pos[0] and self.grid_pos[1] + 1 == block.grid_pos[1]):
            #if (self.tetromino.game.grid.get_tile(block.grid_pos[0], block.grid_pos[1] + 1).occupied == True):
                return False
        return True

    def update(self, *args, **kwargs):
        self.next_pos = self.grid_pos.copy()

    def draw(self, surface, *args, **kwargs):
        surface.blit(self.img, (self.grid_pos[0] * self.size, self.grid_pos[1] * self.size+200))

O_IMG = pygame.image.load('assets/TetrominoO.png')
class TetrominoO(Tetromino):
    def __init__(self, game, start_pos,  size):
        super().__init__(game, start_pos, 'O', O_IMG, size)

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)

    def rotate(self, dir):
        '''
        Does not rotate
        '''
        pass

L_IMG = pygame.image.load('assets/TetrominoL.png')
class TetrominoL(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'L', L_IMG, size)

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 2], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 2], self.size)
        self.blocks.append(block)

J_IMG = pygame.image.load('assets/TetrominoJ.png')
class TetrominoJ(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'J', J_IMG, size)

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 2], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 2], self.size)
        self.blocks.append(block)

S_IMG = pygame.image.load('assets/TetrominoS.png')
class TetrominoS(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'S', S_IMG, size)

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 3):
            start_pos = self.game.grid.width - 3
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 1], self.size)
        self.blocks.append(block)

Z_IMG = pygame.image.load('assets/TetrominoZ.png')
class TetrominoZ(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'Z', Z_IMG, size)

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 3):
            start_pos = self.game.grid.width - 3
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1] + 1], self.size)
        self.blocks.append(block)

T_IMG = pygame.image.load('assets/TetrominoT.png')
class TetrominoT(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'T', T_IMG, size)

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        self.pivot = block
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)

    def rotate(self, dir):
        #update the pivot's next pos first
        self.pivot.next_pos = self.pivot.grid_pos.copy()
        if (self.rotation == 0):
            self.blocks[0].next_pos[0] = self.pivot.next_pos[0]
            self.blocks[0].next_pos[1] = self.pivot.next_pos[1] - dir

            self.blocks[2].next_pos[0] = self.pivot.next_pos[0]
            self.blocks[2].next_pos[1] = self.pivot.next_pos[1] + dir

            self.blocks[3].next_pos[0] = self.pivot.next_pos[0] - dir
            self.blocks[3].next_pos[1] = self.pivot.next_pos[1]
        elif(self.rotation == 1):
            self.blocks[0].next_pos[0] = self.pivot.next_pos[0] + dir
            self.blocks[0].next_pos[1] = self.pivot.next_pos[1]

            self.blocks[2].next_pos[0] = self.pivot.next_pos[0] - dir
            self.blocks[2].next_pos[1] = self.pivot.next_pos[1]

            self.blocks[3].next_pos[0] = self.pivot.next_pos[0]
            self.blocks[3].next_pos[1] = self.pivot.next_pos[1] - dir
        elif(self.rotation == 2):
            self.blocks[0].next_pos[0] = self.pivot.next_pos[0]
            self.blocks[0].next_pos[1] = self.pivot.next_pos[1] - dir

            self.blocks[2].next_pos[0] = self.pivot.next_pos[0]
            self.blocks[2].next_pos[1] = self.pivot.next_pos[1] + dir

            self.blocks[3].next_pos[0] = self.pivot.next_pos[0] + dir
            self.blocks[3].next_pos[1] = self.pivot.next_pos[1]
        elif(self.rotation == 3):
            self.blocks[0].next_pos[0] = self.pivot.next_pos[0] - dir
            self.blocks[0].next_pos[1] = self.pivot.next_pos[1]

            self.blocks[2].next_pos[0] = self.pivot.next_pos[0] + dir
            self.blocks[2].next_pos[1] = self.pivot.next_pos[1]

            self.blocks[3].next_pos[0] = self.pivot.next_pos[0]
            self.blocks[3].next_pos[1] = self.pivot.next_pos[1] + dir
        # todo
        #  rotation check
        #  if rotation check passes
        rotation_passed = True
        for block in self.blocks:
            if(rotation_passed):
                block.grid_pos = block.next_pos.copy()
            block.next_pos = block.grid_pos.copy()
        if (rotation_passed):
            self.rotation = (self.rotation + dir)%4


I_IMG = pygame.image.load('assets/TetrominoI.png')
class TetrominoI(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'I', I_IMG, size)

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 1):
            start_pos = self.game.grid.width - 1
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 2], self.size)
        self.blocks.append(block)
        self.pivot = block
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 3], self.size)
        self.blocks.append(block)

    def rotate(self, dir):
        if(self.rotation == 0):
            self.blocks[0].grid_pos[0] = self.pivot.grid_pos[0] + dir*2
            self.blocks[0].grid_pos[1] = self.pivot.grid_pos[1]

            self.blocks[1].grid_pos[0] = self.pivot.grid_pos[0] + dir
            self.blocks[1].grid_pos[1] = self.pivot.grid_pos[1]

            self.blocks[3].grid_pos[0] = self.pivot.grid_pos[0] - dir
            self.blocks[3].grid_pos[1] = self.pivot.grid_pos[1]
            self.rotation = dir
        else:
            self.blocks[0].grid_pos[0] = self.pivot.grid_pos[0]
            self.blocks[0].grid_pos[1] = self.pivot.grid_pos[1] - 2

            self.blocks[1].grid_pos[0] = self.pivot.grid_pos[0]
            self.blocks[1].grid_pos[1] = self.pivot.grid_pos[1] - 1

            self.blocks[3].grid_pos[0] = self.pivot.grid_pos[0]
            self.blocks[3].grid_pos[1] = self.pivot.grid_pos[1] + 1
            self.rotation = 0

