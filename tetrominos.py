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
        self.update_ghost_blocks()
        self.rotation = 0
        self.falling = True

        # self.fall_delay = 15
        self.fall_delay = 20
        self.last_fall = 0

        self.move_delay = 5
        self.last_move = self.move_delay

        self.soft_drop_delay = 5
        self.last_soft_drop = self.soft_drop_delay

        self.max_stop_fall_delay = 60
        self.stop_fall_delay =  self.max_stop_fall_delay
        self.last_stop_fall = self.stop_fall_delay

        self.blink = False
        self.blink_speed = 0
        self.blink_timer = 0
        self.blink_frame = 0

        self.controllable = True

        self.start_expire = False
        self.max_expire_time = 0

        self.push_matrix = {
            (0, 1): [(-1, 0), (-1, 1), (0, -2), (-1, -2)],
            (1, 0): [(1, 0), (1, -1), (0, 2), (1, 2)],
            (1, 2): [(1, 0), (1, -1), (0, 2), (1, 2)],
            (2, 1): [(-1, 0), (-1, 1), (0, -2), (1, -2)],
            (2, 3): [(1, 0), (1, 1), (0, -2), (1, -2)],
            (3, 2): [(-1, 0), (-1, -1), (0, 2), (-1, 2)],
            (3, 0): [(-1, 0), (-1, -1), (0, 2), (-1, 2)],
            (0, 3): [(1, 0), (1, 1), (0, -2), (1, -2)]
        }
    # (-2, 0)(+1, 0)(-2, -1)(+1, +2)
    # (+2, 0)(-1, 0)(+2, +1)(-1, -2)
    # (-1, 0)(+2, 0)(-1, +2)(+2, -1)
    # (+1, 0)(-2, 0)(+1, -2)(-2, +1)
    # (+2, 0)(-1, 0)(+2, +1)(-1, -2)
    # (-2, 0)(+1, 0)(-2, -1)(+1, +2)
    # (+1, 0)(-2, 0)(+1, -2)(-2, +1)
    # (-1, 0)(+2, 0)(-1, +2)(+2, -1)

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
        self.update_ghost_blocks()

    def soft_drop(self):
        self.fall()
        self.last_soft_drop = 0

    def fall(self):
        for block in self.blocks:
            block.fall()
        if(self.stop_fall_delay < self.max_stop_fall_delay):
            self.stop_fall_delay = min(self.stop_fall_delay + 1, self.max_stop_fall_delay)
        self.update_ghost_blocks()

    def find_landing_spot(self):
        distance = None
        for block in self.blocks:
            block_distance = block.find_fall_distance()
            if(distance is None or block_distance<distance):
                distance = block_distance
        return distance

    def rotate(self, dir):
        '''
        Rotates the tetromino
        :param dir:
        1 = Clockwise
        -1 = Counter clockwise
        :return:
        '''
        # index of next rotation
        next_rotation = (self.rotation + dir) % len(self.rotations)
        self.get_next_rotation_pos(next_rotation)

        rotation_passed = self.check_valid_pos()

        if (not rotation_passed):
            rotation_passed = self.rotation_push(next_rotation)

        for i in range(len(self.blocks)):
            # update each block to next position
            if (rotation_passed):
                block = self.blocks[i]
                # block.grid_pos[0] = next_pos_lst[i][0]
                # block.grid_pos[1] = next_pos_lst[i][1]
                block.go_to_next_pos()
            # block.next_pos = block.grid_pos.copy()
        if (rotation_passed):
            self.rotation = next_rotation
            # if(not self.falling):
            #     self.stop_fall_delay = self.stop_fall_delay-10
            #     self.last_stop_fall = self.stop_fall_delay
        self.update_ghost_blocks()

    def hard_drop(self):
        fall_counter = 0
        while (self.can_fall()):
            self.fall()
            fall_counter = fall_counter + 1
        self.stop_fall()

        if (fall_counter > 5):
            self.game.grid.tile_shake(4 + fall_counter * 0.4, (2, 2))
            self.game.grid.screen_shake(4 + fall_counter * 0.4, (1, 1 + 0.75 * fall_counter))
        else:
            self.game.grid.tile_shake(fall_counter, (2, 2))
            self.game.grid.screen_shake(fall_counter, (0, 2))

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
        self.controllable = False
        self.stop_blink()
        self.expire_timer = 10
        self.start_expire = True

    def expire(self):
        '''
        delete the tetromino
        :return:
        '''
        # release blocks into tiles
        for block in self.blocks:
            tile = self.game.grid.get_tile(block.grid_pos[0], block.grid_pos[1])
            if (tile is not None):
                # self.game.block_lst.append(block)
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
            # left
            if (block.next_pos[0] >= self.game.grid.width):
                return False
            # right
            if (block.next_pos[0] < 0):
                return False
            # bottom
            if (block.next_pos[1] >= self.game.grid.height):
                return False
            if (self.game.grid.get_tile(block.next_pos[0], block.next_pos[1]) is not None):
                if (self.game.grid.get_tile(block.next_pos[0], block.next_pos[1]).occupied == True):
                    return False
        return True

    # deprecated
    def check_move(self, dir):
        for block in self.blocks:
            if (block.grid_pos[0] + dir > self.game.grid.width - 1 or block.grid_pos[0] + dir < 0):
                return False
            if (self.game.grid.get_tile(block.grid_pos[0] + dir, block.grid_pos[1]) is not None):
                if (self.game.grid.get_tile(block.grid_pos[0] + dir, block.grid_pos[1]).occupied == True):
                    return False
        return True

    def get_next_rotation_pos(self, next_rotation):
        # list of block positions for next rotations
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

    def rotation_push(self, next_rotation):
        '''
        Tries to find a valid spot for the tetromino to rotate into
        :return:True if a valid rotation spot can be found
        False if no valid rotation spots are found
        '''
        rot_tuple = (self.rotation, next_rotation)
        # save next position
        blocks_next_pos = []
        for block in self.blocks:
            blocks_next_pos.append(block.next_pos.copy())

        for test in self.push_matrix[rot_tuple]:
            print(test)
            for i in range(0,len(self.blocks)):
                block = self.blocks[i]
                block.next_pos[0] = blocks_next_pos[i][0] + test[0]
                block.next_pos[1] = blocks_next_pos[i][1] + test[1]
            if (self.check_valid_pos() == True):
                return True

        # #kick 1 space right
        # for block in self.blocks:
        #     block.next_pos[0] = block.next_pos[0] - 1
        # if(self.check_valid_pos()==True):
        #     return True
        # #kick 1 space left
        # for block in self.blocks:
        #     block.next_pos[0] = block.next_pos[0] +2
        # if(self.check_valid_pos()==True):
        #     return True

        # i piece never kicks

        return False

    def start_blink(self, speed):
        self.blink = True
        self.blink_speed = speed
        self.blink_frame = 1

    def stop_blink(self):
        self.blink = False
        self.blink_speed = 0
        self.blink_frame = 0

    def update_ghost_blocks(self):
        distance = self.find_landing_spot()
        for block in self.blocks:
            block.ghost_block.distance = distance

    def update(self, *args, **kwargs):
        if (self.start_expire):
            self.expire_timer -= 1
            if (self.expire_timer <= 0):
                self.expire()
            return
        # horizontal -> rotation -> soft drop/normal fall -> hard drop

        # set each block's next pos to its current pos
        for block in self.blocks:
            block.next_pos = block.grid_pos.copy()

        if (self.controllable):
            # horizontal movement
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

            # rotation
            for event in args[1]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.rotate(-1)
                    if event.key == pygame.K_x:
                        self.rotate(1)

        # falling and soft drop
        if (self.falling == True):
            # stop falling check
            if (self.can_fall() == False):
                self.falling = False
                return
            self.last_fall = self.last_fall + 1
            # soft drop
            if (args[0][pygame.K_DOWN] == True and self.last_soft_drop >= self.soft_drop_delay):
                self.soft_drop()
                self.last_fall = 0
            elif (self.last_fall >= self.fall_delay):
                self.fall()
                self.last_fall = 0
        else:
            print('cannot fall ' + str(self.last_stop_fall))
            self.last_stop_fall = self.last_stop_fall - 1
            self.stop_fall_delay -= 0.5
            if (self.last_stop_fall == 25):
                self.start_blink(6)
            if (self.last_stop_fall == 10):
                self.start_blink(3)
            if (self.can_fall() == True):
                self.falling = True
                self.last_stop_fall = self.stop_fall_delay
                self.stop_blink()
            elif (self.last_stop_fall <= 0):
                self.stop_fall()
            # add delay before stop_fall is called
            # set falling back to True if the tetromino can fall again

        # hard drop
        if (self.controllable):
            for event in args[1]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # print('key up')
                        self.hard_drop()
                        return

    def draw(self, surface, *args, **kwargs):
        frame = 0
        if (self.blink):
            if (self.blink_timer >= self.blink_speed):
                self.blink_frame = (self.blink_frame + 1) % 2
                self.blink_timer = 0
            self.blink_timer = self.blink_timer + 1
            frame = self.blink_frame
        for block in self.blocks:
            block.ghost_block.draw(surface)
        for block in self.blocks:
            block.draw(surface, frame)

class TetrominoBlock:
    def __init__(self, tetromino, grid_pos, size):
        self.tetromino = tetromino
        # self.img = self.tetromino.img
        # self.blink_img = pygame.image.load('assets/Blink Tetrominos/Tetromino' + str(self.tetromino.type) + '.png')

        if(self.tetromino is not None):
            self.img_lst = self.tetromino.img

        self.grid_pos = grid_pos
        self.next_pos = self.grid_pos.copy()
        self.ghost_block = GhostTetrominoBlock(self.img_lst[2], self)
        self.size = size

    def go_to_next_pos(self):
        self.grid_pos = self.next_pos.copy()
        self.next_pos = self.grid_pos.copy()

    def fall(self):
        self.grid_pos[1] = self.grid_pos[1] + 1

    def can_fall(self, pos = None):
        if (pos == None):
            pos = self.grid_pos
        if (pos[1] + 1 >= self.tetromino.game.grid.height):
            return False

        # for block in self.tetromino.game.block_lst:
        #     if (self.grid_pos[0] == block.grid_pos[0] and self.grid_pos[1] + 1 == block.grid_pos[1]):
        if (self.tetromino.game.grid.get_tile(pos[0], pos[1] + 1) is not None):
            if (self.tetromino.game.grid.get_tile(pos[0], pos[1] + 1).occupied == True):
                return False
        return True

    def find_fall_distance(self):
        fall_counter = 0
        while (self.can_fall((self.grid_pos[0], self.grid_pos[1] + fall_counter))):
            fall_counter = fall_counter + 1
        return fall_counter

    def update(self, *args, **kwargs):
        # self.next_pos = self.grid_pos.copy()
        pass

    def draw(self, surface, img_id=0, *args, **kwargs):
        surface.blit(self.img_lst[img_id], (self.grid_pos[0] * self.size, self.grid_pos[1] * self.size))

GARBAGE_IMG = [pygame.image.load('assets/Garbage Block.png'),
         pygame.image.load('assets/Blink Tetrominos/Garbage Block.png'),
         pygame.image.load('assets/Ghost Tetrominos/Garbage Block.png')
         ]
class GarbageBlock(TetrominoBlock):
    def __init__(self, grid_pos, size):
        self.img_lst = GARBAGE_IMG
        super().__init__(None, grid_pos, size)

class GhostTetrominoBlock():
    def __init__(self, img, block):
        self.img = img
        self.block = block
        self.distance = 0

    def draw(self, surface, *args, **kwargs):
        surface.blit(self.img,
                    (self.block.grid_pos[0] * self.block.size,
                    (self.block.grid_pos[1] + self.distance) * self.block.size))

O_IMG = [pygame.image.load('assets/TetrominoO.png'),
         pygame.image.load('assets/Blink Tetrominos/TetrominoO.png'),
         pygame.image.load('assets/Ghost Tetrominos/TetrominoO.png')
         ]

class TetrominoO(Tetromino):
    def __init__(self, game, start_pos, size):
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

L_IMG = [pygame.image.load('assets/TetrominoL.png'),
         pygame.image.load('assets/Blink Tetrominos/TetrominoL.png'),
         pygame.image.load('assets/Ghost Tetrominos/TetrominoL.png')
         ]

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


J_IMG = [pygame.image.load('assets/TetrominoJ.png'),
         pygame.image.load('assets/Blink Tetrominos/TetrominoJ.png'),
         pygame.image.load('assets/Ghost Tetrominos/TetrominoJ.png')
         ]

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


S_IMG = [pygame.image.load('assets/TetrominoS.png'),
         pygame.image.load('assets/Blink Tetrominos/TetrominoS.png'),
         pygame.image.load('assets/Ghost Tetrominos/TetrominoS.png')
         ]

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


Z_IMG = [pygame.image.load('assets/TetrominoZ.png'),
         pygame.image.load('assets/Blink Tetrominos/TetrominoZ.png'),
         pygame.image.load('assets/Ghost Tetrominos/TetrominoZ.png')
         ]

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


T_IMG = [pygame.image.load('assets/TetrominoT.png'),
         pygame.image.load('assets/Blink Tetrominos/TetrominoT.png'),
         pygame.image.load('assets/Ghost Tetrominos/TetrominoT.png')
         ]

class TetrominoT(Tetromino):
    def __init__(self, game, start_pos, size):
        super().__init__(game, start_pos, 'T', T_IMG, size)
        self.rotations = (
            # rotation 2
            #    3
            # 2 [1] 0
            ((1, 0), (0, 0), (-1, 0), (0, -1)),
            # rotation 3
            #  0
            # [1] 3
            #  2
            ((0, -1), (0, 0), (0, 1), (1, 0)),
            # rotation 0
            # 0 [1] 2
            #    3
            ((-1, 0), (0, 0), (1, 0), (0, 1)),
            # rotation 1
            #    0
            # 3 [1]
            #    2
            ((0, -1), (0, 0), (0, 1), (-1, 0)),
        )
        self.pivot_index = 1

    def create_blocks(self, start_pos):
        if (start_pos[0] < 0):
            start_pos = 0
        if (start_pos[0] > self.game.grid.width - 2):
            start_pos = self.game.grid.width - 2
        # 0 [1] 2
        #    3

        #    3
        # 2 [1] 0
        block = TetrominoBlock(self, [start_pos[0] + 2, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0], start_pos[1]], self.size)
        self.blocks.append(block)
        block = TetrominoBlock(self, [start_pos[0] + 1, start_pos[1] - 1], self.size)
        self.blocks.append(block)


I_IMG = [pygame.image.load('assets/TetrominoI.png'),
         pygame.image.load('assets/Blink Tetrominos/TetrominoI.png'),
         pygame.image.load('assets/Ghost Tetrominos/TetrominoI.png')
         ]


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
        self.push_matrix = {
            (0, 1): [(-2, 0), (1, 0), (-2, -1), (1, 2)],
            (1, 0): [(2, 0), (-1, 0), (2, 1), (-1, -2)],
            (1, 2): [(-1, 0), (2, 0), (-1, 2), (2, -1)],
            (2, 1): [(1, 0), (-2, 0), (1, -2), (-2, 1)],
            (2, 3): [(2, 0), (-1, 0), (2, 1), (-1, -2)],
            (3, 2): [(-2, 0), (1, 0), (-2, -1), (1, 2)],
            (3, 0): [(1, 0), (-2, 0), (1, -2), (-2, 1)],
            (0, 3): [(-1, 0), (2, 0), (-1, 2), (2, -1)]
        }

    def get_next_rotation_pos(self, next_rotation):
        super().get_next_rotation_pos(next_rotation)
        for block in self.blocks:
            if (self.rotation == 0 and next_rotation == 1):
                block.next_pos[0] = block.next_pos[0] + 1
            if (self.rotation == 1 and next_rotation == 2):
                block.next_pos[1] = block.next_pos[1] + 1
            if (self.rotation == 2 and next_rotation == 3):
                block.next_pos[0] = block.next_pos[0] - 1
            if (self.rotation == 3 and next_rotation == 0):
                block.next_pos[1] = block.next_pos[1] - 1

            if (self.rotation == 1 and next_rotation == 0):
                block.next_pos[0] = block.next_pos[0] - 1
            if (self.rotation == 2 and next_rotation == 1):
                block.next_pos[1] = block.next_pos[1] - 1
            if (self.rotation == 3 and next_rotation == 2):
                block.next_pos[0] = block.next_pos[0] + 1
            if (self.rotation == 0 and next_rotation == 3):
                block.next_pos[1] = block.next_pos[1] + 1

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
