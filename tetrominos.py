import pygame.image

class Tetromino:
    def __init__(self, game, start_pos, type, img, size):
        self.game = game
        self.type = type
        self.img = img
        self.size = size
        self.rotations = ()
        self.blocks = []
        self.pivot_index = 0
        self.create_blocks(start_pos)
        self.rotation = 0
        self.falling = True

        # self.fall_delay = 15
        self.fall_delay = 20
        self.last_fall = 0

        self.move_delay = 5
        self.last_move = self.move_delay

        self.soft_drop_delay = 5
        self.last_soft_drop = self.soft_drop_delay

        self.stop_fall_delay = 30
        self.last_stop_fall = self.stop_fall_delay

    def create_blocks(self, start_pos):
        pass

    def move(self, dir):
        # if (self.check_move(dir) == True):
        #     for block in self.blocks:
        #         block.grid_pos[0] = block.grid_pos[0] + dir
        #     self.last_move = 0
        for block in self.blocks:
            block.next_pos[0] = block.grid_pos[0] + dir
        if (self.check_valid_pos() == True):
            for block in self.blocks:
                block.go_to_next_pos()
            block.next_pos = block.grid_pos.copy()
            self.last_move = 0

    def soft_drop(self):
        self.fall()
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

        next_rotation = (self.rotation + dir) % len(self.rotations)
        rotation_lst = self.rotations[next_rotation]
        # print(next_rotation)
        # print(rotation_lst)
        pivot_pos = self.blocks[self.pivot_index].grid_pos.copy()
        # next_pos_lst = []
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            # print( rotation_lst[i])
            block.next_pos[0] = pivot_pos[0] + rotation_lst[i][0]
            block.next_pos[1] = pivot_pos[1] + rotation_lst[i][1]
            # next_pos_lst.append([pivot_pos[0] + rotation_lst[i][0], pivot_pos[1] + rotation_lst[i][1]])
        # todo
        #  rotation check
        #  if rotation check passes

        rotation_passed = self.check_valid_pos()
        if(not rotation_passed):
            rotation_passed = self.rotation_push()

        for i in range(len(self.blocks)):
            if (rotation_passed):
                block = self.blocks[i]
                # block.grid_pos[0] = next_pos_lst[i][0]
                # block.grid_pos[1] = next_pos_lst[i][1]
                block.go_to_next_pos()
            block.next_pos = block.grid_pos.copy()
        if (rotation_passed):
            self.rotation = next_rotation
            # if(not self.falling):
            #     self.stop_fall_delay = self.stop_fall_delay-10
            #     self.last_stop_fall = self.stop_fall_delay

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
        #release blocks into tiles
        for block in self.blocks:
            tile = self.game.grid.get_tile(block.grid_pos[0], block.grid_pos[1])
            if(tile is not None):
                #self.game.block_lst.append(block)
                tile.block = block
                tile.occupied = True
            else:
                self.game.out_of_bounds_block()
        self.game.control_tetromino = None
        self.game.grid.check_filled_rows = True

    def check_valid_pos(self):
        '''
        Checks that the next position of each block in the tetromino is in a valid position
        (not outside the grid or in another block)
        :return: True if valid, False otherwise
        '''
        for block in self.blocks:
            #left
            if (block.next_pos[0] >= self.game.grid.width):
                return False
            #right
            if (block.next_pos[0] < 0):
                return False
            #bottom
            if (block.next_pos[1] >= self.game.grid.height):
                return False
            if (self.game.grid.get_tile(block.next_pos[0], block.next_pos[1]) is not None):
                if (self.game.grid.get_tile(block.next_pos[0], block.next_pos[1]).occupied == True):
                    return False
        return True

    #deprecated
    def check_move(self, dir):
        for block in self.blocks:
            if (block.grid_pos[0] + dir > self.game.grid.width - 1 or block.grid_pos[0] + dir < 0):
                return False
            if (self.game.grid.get_tile(block.grid_pos[0] + dir, block.grid_pos[1]) is not None):
                if (self.game.grid.get_tile(block.grid_pos[0] + dir, block.grid_pos[1]).occupied == True):
                    return False
        return True

    def rotation_push(self):
        '''
        Tries to find a valid spot for the tetromino to rotate into
        :return:True if a valid rotation spot can be found
        False if no valid rotation spots are found
        '''
        #todo
        # improve push accuracy
        #push block out
        for block in self.blocks:
            block.next_pos[0] = block.next_pos[0] - 1
        if(self.check_valid_pos()==True):
            return True
        for block in self.blocks:
            block.next_pos[0] = block.next_pos[0] + 2
        if(self.check_valid_pos()==True):
            return True
        return False

    def update(self, *args, **kwargs):
        #horizontal -> rotation -> soft drop/normal fall -> hard drop

        #set each block's next pos to its current pos
        for block in self.blocks:
            block.next_pos = block.grid_pos.copy()
        #horizontal movement
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

        #rotation
        for event in args[1]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.rotate(-1)
                if event.key == pygame.K_x:
                    self.rotate(1)

        #falling and soft drop
        if (self.falling == True):
            #stop falling check
            if (self.can_fall() == False):
                self.falling = False
                return
            self.last_fall = self.last_fall + 1
            #soft drop
            if (args[0][pygame.K_DOWN] == True and self.last_soft_drop >= self.soft_drop_delay):
                self.soft_drop()
                self.last_fall = 0
            elif(self.last_fall >= self.fall_delay):
                self.fall()
                self.last_fall = 0
        else:
            self.last_stop_fall = self.last_stop_fall - 1
            if(self.can_fall() == True):
                self.falling = True
                self.last_stop_fall = self.stop_fall_delay
            elif(self.last_stop_fall <= 0):
                self.stop_fall()
            # add delay before stop_fall is called
            # set falling back to True if the tetromino can fall again

        #hard drop
        for event in args[1]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # print('key up')
                    self.hard_drop()
                    return

    def draw(self, surface, *args, **kwargs):
        for block in self.blocks:
            block.draw(surface)


class TetrominoBlock:
    def __init__(self, tetromino, grid_pos, size):
        self.tetromino = tetromino
        self.img = self.tetromino.img
        self.blink_img = pygame.image.load('assets/Blink Tetrominos/Tetromino' + str(self.tetromino.type) + '.png')
        self.blink = False
        self.blink_timer = 0
        self.grid_pos = grid_pos
        self.next_pos = self.grid_pos.copy()
        self.size = size

    def go_to_next_pos(self):
        self.grid_pos = self.next_pos.copy()
        self.next_pos = self.grid_pos.copy()

    def fall(self):
        self.grid_pos[1] = self.grid_pos[1] + 1

    def can_fall(self):
        if (self.grid_pos[1] + 1 >= self.tetromino.game.grid.height):
            return False

        # for block in self.tetromino.game.block_lst:
        #     if (self.grid_pos[0] == block.grid_pos[0] and self.grid_pos[1] + 1 == block.grid_pos[1]):
        if (self.tetromino.game.grid.get_tile(self.grid_pos[0], self.grid_pos[1] + 1) is not None):
            if (self.tetromino.game.grid.get_tile(self.grid_pos[0], self.grid_pos[1] + 1).occupied == True):
                return False
        return True

    def update(self, *args, **kwargs):
        # self.next_pos = self.grid_pos.copy()
        pass

    def draw(self, surface, *args, **kwargs):
        if(self.blink == True):
            surface.blit(self.blink_img, (self.grid_pos[0] * self.size, self.grid_pos[1] * self.size))
        else:
            surface.blit(self.img, (self.grid_pos[0] * self.size, self.grid_pos[1] * self.size))

O_IMG = pygame.image.load('assets/TetrominoO.png')
class TetrominoO(Tetromino):
    def __init__(self, game, start_pos,  size):
        super().__init__(game, start_pos, 'O', O_IMG, size)
        self.rotations = (
            # rotation 0
            # [0] 1
            #  2  3
            ((0, 0), (1, 0), (1, 1), (0, 1)),
        )
        self.pivot_index = 0

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 1], self.size)
        self.blocks.append(block)

L_IMG = pygame.image.load('assets/TetrominoL.png')
class TetrominoL(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'L', L_IMG, size)
        self.rotations = (
            # rotation 0
            #       0
            # 3 [2] 1
            ((1, -1), (1, 0), (0, 0), (-1, 0)),
            # rotation 1
            #  3
            # [2]
            #  1  0
            ((1, 1), (0, 1), (0, 0), (0, -1)),
            # rotation 2
            #   [2] 3
            # 0  1
            ((-1, 1), (-1, 0), (0, 0), (1, 0)),
            # rotation 3
            # 0
            # 1 [2]
            #    3
            ((-1, -1), (0, -1), (0, 0), (0, 1)),
        )
        self.pivot_index = 2

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 1], self.size)
        self.blocks.append(block)

J_IMG = pygame.image.load('assets/TetrominoJ.png')
class TetrominoJ(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'J', J_IMG, size)
        self.rotations = (
            # rotation 0
            # 0
            # 1 [2] 3
            ((-1, -1), (-1, 0), (0, 0), (1, 0)),
            # rotation 1
            #  1  0
            # [2]
            #  3
            ((1, -1), (0, -1), (0, 0), (0, 1)),
            # rotation 2
            # 3 [2] 1
            #       0
            ((1, 1), (1, 0), (0, 0), (-1, 0)),
            # rotation 3
            #    3
            #   [2]
            # 0  1
            ((-1, 1), (0, 1), (0, 0), (0, -1)),
        )
        self.pivot_index = 2

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1] + 1], self.size)
        self.blocks.append(block)

S_IMG = pygame.image.load('assets/TetrominoS.png')
class TetrominoS(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'S', S_IMG, size)
        self.rotations = (
            # rotation 0
            #    1  0
            # 3 [2]
            ((1, -1), (0, -1), (0, 0), (-1, 0)),
            # rotation 1
            #  3
            # [2] 1
            #     0
            ((1, 1), (1, 0), (0, 0), (0, -1)),
            # rotation 2
            #   [2] 3
            # 0  1
            ((-1, 1), (0, 1), (0, 0), (1, 0)),
            # rotation 3
            # 0
            # 1 [2]
            #    3
            ((-1, -1), (-1, 0), (0, 0), (0, 1)),
        )
        self.pivot_index = 2

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 3):
            start_pos = self.game.grid.width - 3
        #    1  0
        # 3 [2]
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
        self.rotations = (
            # rotation 0
            # 0  1
            #   [2] 3
            ((-1, -1), (0, -1), (0, 0), (1, 0)),
            # rotation 1
            #     0
            # [2] 1
            #  3
            ((1, -1), (1, 0), (0, 0), (0, 1)),
            # rotation 2
            # 3 [2]
            #    1  0
            ((1, 1), (0, 1), (0, 0), (-1, 0)),
            # rotation 3
            #    3
            # 1 [2]
            # 0
            ((-1, 1), (-1, 0), (0, 0), (0, -1)),
        )
        self.pivot_index = 2

    def create_blocks(self, start_pos):
        # 0  1
        #   [2] 3
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 3):
            start_pos = self.game.grid.width - 3
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1] + 1], self.size)
        self.blocks.append(block)

T_IMG = pygame.image.load('assets/TetrominoT.png')
class TetrominoT(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'T', T_IMG, size)
        self.rotations = (
            # rotation 0
            # 0 [1] 2
            #    3
            ((-1, 0), (0, 0), (1, 0), (0, 1)),
            # rotation 1
            #    0
            # 3 [1]
            #    2
            ((0, -1), (0, 0), (0, 1), (-1, 0)),
            # rotation 2
            #    3
            # 2 [1] 0
            ((1,0),(0,0),(-1,0),(0,-1)),
            # rotation 3
            #  0
            # [1] 3
            #  2
            ((0,-1),(0,0),(0,1),(1,0)),
        )
        self.pivot_index = 1

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        # 0 [1] 2
        #    3
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] + 1], self.size)
        self.blocks.append(block)


I_IMG = pygame.image.load('assets/TetrominoI.png')
class TetrominoI(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'I', I_IMG, size)
        self.rotations = (
            # rotation 0
            # 0 [1] 2  3
            ((-1, 0), (0, 0), (1, 0), (2, 0)),
            # rotation 1
            #  0
            # [1]
            #  2
            #  3
            ((0, -1), (0, 0), (0, 1), (0, 2)),
            # rotation 2
            # 3  2 [1] 0
            ((1, 0), (0, 0), (-1, 0), (-2, 0)),
            # rotation 3
            #  3
            #  2
            # [1]
            #  0
            ((0, 1), (0, 0), (0, -1), (0, -2)),
        )
        self.pivot_index = 1

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 1):
            start_pos = self.game.grid.width - 1
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 3, start_pos[1]], self.size)
        self.blocks.append(block)

