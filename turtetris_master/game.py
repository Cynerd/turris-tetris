import time
from random import randrange


SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

COLORS = [
    'black',
    'FF5500',
    '64C873',
    '786CF5',
    'FF8C32',
    '327834',
    '92CA49',
    '96A1DA'
]


class Game:
    "game it self"

    def __init__(self, matrix):
        self.matrix = matrix
        matrix.fill('black')  # Clear game area
        self.mx = [None]*(matrix.width - 2)
        for i in range(len(self.mx)):
            self.mx[i] = [0]*matrix.height
        self.stone_next = SHAPES[randrange(len(SHAPES))][:]
        # Don't have to check result as it should always be successful
        if not self.new_stone():
            raise Exception('New game but we can\'t place stone')
        self.step = 0
        self.step_edge = 60
        self.score = 0
        self.__show_score__()
        matrix.display()

    def new_stone(self):
        "Create new stone to next one and move next one to stone"
        self.stone = self.stone_next
        self.stone_next = SHAPES[randrange(len(SHAPES))][:]  # Note: we do copy
        # Render stone on top
        self.stone_x = 4
        self.stone_y = 0
        if self.__check_collision__(self.stone_x, self.stone_y, self.stone):
            # locate different place
            self.stone_x = 0
            while self.stone_x < (self.matrix.width - 2) and \
                self.__check_collision__(self.stone_x, self.stone_y,
                                         self.stone):
                self.stone_x += 1
        if self.stone_x >= (self.matrix.width - 2):
            # Than game over
            return False
        self.__render_stone__()
        # Render next stone
        for x in range(2):
            for y in range(4):
                if (x < len(self.stone_next) and y < len(self.stone_next[x])
                        and self.stone_next[x][y] != 0):
                    self.matrix.pixel(self.matrix.width - 1 - x,
                                      self.matrix.height - 1 - y,
                                      'red')
                else:
                    self.matrix.pixel(self.matrix.width - 1 - x,
                                      self.matrix.height - 1 - y,
                                      'black')
        return True

    def __render_stone__(self):
        "Render stone"
        for x in range(len(self.stone)):
            for y in range(len(self.stone[x])):
                if self.stone[x][y] != 0:
                    self.matrix.pixel(self.matrix.width - x - 3 - self.stone_x,
                                      self.matrix.height - 1 - y - self.stone_y,
                                      COLORS[self.stone[x][y]])

    def __clear_stone__(self):
        "Clear rendered stone"
        for x in range(len(self.stone)):
            for y in range(len(self.stone[x])):
                if self.stone[x][y] != 0:
                    self.matrix.pixel(self.matrix.width - x - 3 - self.stone_x,
                                      self.matrix.height - 1 - y - self.stone_y,
                                      'black')

    def __check_collision__(self, x, y, stone):
        "Check if stone collides. Returns True of so."
        for a in range(len(stone)):
            for b in range(len(stone[a])):
                sx = len(self.mx) - 1 - a - x
                sy = len(self.mx[a]) - 1 - b - y
                if stone[a][b] != 0 and (
                        sx < 0 or sy < 0 or
                        sx >= len(self.mx) or sy >= len(self.mx[a]) or
                        self.mx[sx][sy] != 0):
                    return True
        return False

    def __show_score__(self):
        "Show score in bottom right"
        pass

    def __place__(self):
        "Stone can't move so place it, check lines and generate new one"
        for x in range(len(self.stone)):
            for y in range(len(self.stone[x])):
                if self.stone[x][y] != 0:
                    sx = len(self.mx) - 1 - x - self.stone_x
                    sy = len(self.mx[0]) - 1 - y - self.stone_y
                    if sy >= len(self.mx[0]) - 1:
                        # Placing in to the top most line means game-over
                        return False
                    self.mx[sx][sy] = self.stone[x][y]
        # Check if we don't potentionally have full line
        y = 0
        while y < len(self.mx[0]):
            x = 0
            while x < len(self.mx) and self.mx[x][y] != 0:
                x += 1
            if x >= len(self.mx):  # We have full line
                # Show red line
                for x in range(len(self.mx)):
                    self.matrix.pixel(x, y, 'red')
                self.matrix.display()
                time.sleep(0.2)
                # Now move all lines down
                for yy in range(y, len(self.mx[0]) - 1):
                    for x in range(len(self.mx)):
                        self.mx[x][yy] = self.mx[x][yy + 1]
                        # Note: mx is already inverted
                        self.matrix.pixel(x, yy, COLORS[self.mx[x][yy]])
                # Make ticks faster
                self.step_edge *= 0.8
                self.score += 1
                self.__show_score__()
            else:
                # Note that this ensures that we check same line again after
                # line is located
                y += 1
        # Create new stone (if possible)
        return self.new_stone()

    def __down__(self):
        "Move stone down"
        new_y = self.stone_y + 1
        if self.__check_collision__(self.stone_x, new_y, self.stone):
            return self.__place__()
        else:
            self.__clear_stone__()
            self.stone_y = new_y
            self.__render_stone__()
            return True

    def __rotate__(self):
        "Rotate stone"
        rotated = [
            [self.stone[y][x] for y in range(len(self.stone))]
            for x in range(len(self.stone[0]) - 1, -1, -1)]
        if not self.__check_collision__(self.stone_x, self.stone_y, rotated):
            self.__clear_stone__()
            self.stone = rotated
            self.__render_stone__()

    def __move__(self, left):
        "Move stone left or right"
        new_x = self.stone_x
        if left:
            new_x += 1
        else:
            new_x -= 1
        if not self.__check_collision__(new_x, self.stone_y, self.stone):
            self.__clear_stone__()
            self.stone_x = new_x
            self.__render_stone__()

    def tick(self, input):
        "Do game tick"
        gameover = False
        if input['up']:
            self.__rotate__()
        if input['left'] != input['right']:
            self.__move__(input['left'])
        if self.step >= self.step_edge or \
           (input['down'] and self.step >= self.step_edge/3):
            gameover = not self.__down__()
            self.step = 0
        else:
            self.step += 1
        self.matrix.display()
        return not gameover
