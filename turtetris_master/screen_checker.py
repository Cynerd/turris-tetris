class ScreenChecker:
    "Simple screen checker showing lines and updates"

    def __init__(self, matrix):
        "Initialize it for given matrix"
        if matrix.height >= matrix.width:
            raise Exception('ScreenChecker doesn\'t support wide matrix.')
        self.matrix = matrix
        self.__tick__ = 0
        self.__pos__ = [[0, 0] for _ in range(matrix.height)]
        for i in range(0, matrix.height):
            self.__pos__[i][1] = i
            for y in range(0, i):
                matrix.pixel(i, y, 'green')

    def __pos_inc__(self, p):
        p += 1
        if p >= self.matrix.width:
            p = 0
        return p

    def tick(self):
        self.__tick__ += 1
        if self.__tick__ > 60:
            self.__tick__ = 0
            for i in range(0, self.matrix.height):
                self.matrix.pixel(self.__pos__[i][0], i, '000000')
                self.__pos__[i][0] = self.__pos_inc__(self.__pos__[i][0])
                self.__pos__[i][1] = self.__pos_inc__(self.__pos__[i][1])
                self.matrix.pixel(self.__pos__[i][1], i, color='green')
            return True
        else:
            return False
