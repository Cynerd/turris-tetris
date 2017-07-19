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
            self.mx[i] = [None]*matrix.height
        self.stone_next = SHAPES[randrange(len(SHAPES))][:]
        # Don't have to check result as it should always be successful
        self.new_stone()
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
        return False

    def __down__(self):
        "Move stone down"
        pass

    def __rotate__(self):
        "Rotate stone"
        pass

    def __move__(self, left):
        "Move stone left or right"
        pass

    def tick(self, input):
        "Do game tick"
        if input['up']:
            self.__rotate__()
        if input['left'] != input['right']:
            self.__move__(input['left'])
        if self.step >= self.step_edge or \
           (input['down'] and self.step >= self.step_edge/2):
            self.__down__()
            self.step = 0
        self.matrix.display()
        return not input['select']
