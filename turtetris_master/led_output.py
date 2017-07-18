import zmq
import json


class Matrix:
    "Leds matrix"

    def __init__(self):
        "Establish connection to matrix"
        self.__mat__ = [[{
            'color': '000000',
            'intens': 0
        }]*12]*10
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind('tcp://*:4444')

    def display(self):
        "Display matrix to leds"
        for i in range(0, 10):
            self.socket.send_string('line' + str(i) + ' ' +
                                    json.dumps(self.__mat__[i]))

    def pixel(self, x, y, color=None, bright=None):
        "Set pixel in matrix"
        if x < 0 or x > 11 or y < 0 or y > 9:
            return  # just ignore any pixel outside of the matrix
        if color is not None:
            self.__mat__[y][x]['color'] = color
        if bright is not None:
            self.__mat__[y][x]['bright'] = bright
