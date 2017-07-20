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
        self.mx = [None]*(matrix.width - 3)
        for i in range(len(self.mx)):
            self.mx[i] = [0]*matrix.height
        self.stone_next = SHAPES[randrange(len(SHAPES))][:]
        # Don't have to check result as it should always be successful
        assert self.new_stone()
        self.step = 0
        self.step_edge = 60
        matrix.display()

    def new_stone(self):
        "Create new stone to next one and move next one to stone"
        self.stone = self.stone_next
        self.stone_next = SHAPES[randrange(len(SHAPES))][:]  # Note: we do copy
        # Render stone on top
        self.stone_x = 3
        self.stone_y = 0
        if self.__check_collision__(self.stone_x, self.stone_y, self.stone):
            # locate different place
            self.stone_x = 0
            while self.stone_x < (self.matrix.width - 3) and \
                self.__check_collision__(self.stone_x, self.stone_y,
                                         self.stone):
                self.stone_x += 1
        if self.stone_x >= (self.matrix.width - 3):
            # Than game over
            return False
        self.__render_stone__()
        # Render next stone
        for x in range(2):
            for y in range(4):
                if x < len(self.stone_next) and y < len(self.stone_next[x]):
                    self.matrix.pixel(11 - x, 9 - y,
                                      COLORS[self.stone_next[x][y]])
                else:
                    self.matrix.pixel(11 - x, 9 - y, 'black')
        return True

    def __render_stone__(self):
        "Render stone"
        for x in range(len(self.stone)):
            for y in range(len(self.stone[x])):
                if self.stone[x][y] != 0:
                    self.matrix.pixel(11 - x - 3 - self.stone_x,
                                      9 - y - self.stone_y,
                                      COLORS[self.stone[x][y]])

    def __clear_stone__(self):
        "Clear rendered stone"
        for x in range(len(self.stone)):
            for y in range(len(self.stone[x])):
                if self.stone[x][y] != 0:
                    self.matrix.pixel(11 - x - 3 - self.stone_x,
                                      9 - y - self.stone_y,
                                      'black')

    def __check_collision__(self, x, y, stone):
        "Check if stone collides. Returns True of so."
        for a in range(len(stone)):
            for b in range(len(stone[a])):
                sx = 11 - a - x
                sy = 9 - b - y
                print("sx:{0} sy:{1} mx:{2}:{3}".format(
                    sx, sy, len(self.mx), len(self.mx[0])
                    ))
                if stone[a][b] != 0 and (
                        sx < 0 or sy < 0 or sx > 11 or sy > 9 or
                        self.mx[sx][sy] != 0):
                    return True
        return False

    def __place__(self):
        "Stone can't move so place it, check lines and generate new one"
        for x in range(len(self.stone)):
            for y in range(len(self.stone[x])):
                if self.stone[x][y] != 0:
                    self.mx[11 - x - self.stone_x][9 - y - self.stone_y] =\
                        self.stone[x][y]
        # TODO Line completion and removal and step division
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

    def __rotate__(self):
        "Rotate stone"
        rotated = [
            [self.stone[y][x] for y in range(len(self.stone))]
            for x in range(len(self.stone[0]) - 1, -1, -1)]
        if not self.__check_collision__(self.stone_x, self.stone_y, rotated):
            self.stone = rotated
            self.__clear_stone__()
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
           (input['down'] and self.step >= self.step_edge/2):
            gameover = self.__down__()
            self.step = 0
        else:
            self.step += 1
        self.matrix.display()
        return not gameover
