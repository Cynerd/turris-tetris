import zmq
import json


class Matrix:
    "Leds matrix"

    def __init__(self):
        "Establish connection to matrix"
        self.width = 12
        self.height = 10
        self.__mat__ = [None]*10
        for x in range(10):
            self.__mat__[x] = [None]*12
            for y in range(12):
                self.__mat__[x][y] = '000000'
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind('tcp://*:4444')

    def display(self):
        "Display matrix to leds"
        for i in range(0, 10):
            self.socket.send_string('line' + str(i) + ' ' +
                                    json.dumps(self.__mat__[i]))

    def pixel(self, x, y, color):
        "Set pixel in matrix"
        if x < 0 or x > 11 or y < 0 or y > 9:
            raise Exception('Pixel out of matrix')
        self.__mat__[y][x] = color
