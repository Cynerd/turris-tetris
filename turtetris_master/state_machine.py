from .screen_checker import ScreenChecker
from .game import Game


class StateMachine:
    "Game state machine"

    def __init__(self, matrix, input):
        "Initializes game machine"
        self.state = "initializing"
        self.matrix = matrix
        self.input = input
        self.__update_state__('screen_checker')

    def __update_state__(self, state):
        "Applies given state"
        def __exception__():
            raise Exception('Can\'t transfer from ' + self.state + ' to '
                            + state)
        if state == "screen_checker":
            if self.state == "initializing":
                self.screen_checker = ScreenChecker(self.matrix)
            else:
                __exception__()
        elif state == "game":
            if self.state == "screen_checker" or self.state == "game-over":
                self.game = Game(self.matrix)
            else:
                __exception__()
        elif state == "game-over":
            if self.state != "game":
                __exception__()
        else:
            __exception__()
        self.state = state

    def tick(self):
        "Do tick"
        inpt = self.input.check()
        if self.state == "screen_checker":
            if inpt['start']:
                self.__update_state__('game')
            else:
                self.screen_checker.tick()
        elif self.state == "game":
            if not self.game.tick(inpt):
                self.__update_state__('game-over')
        elif self.state == "game-over":
            if inpt['start']:
                self.__update_state__('game')
        else:
            raise Exception('Invalid state ' + self.state)
