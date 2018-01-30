from .screen_checker import ScreenChecker
from .game import Game
from .recorder import Recorder
from .recorder import Replayer

# We run 1/30 loops per second so this gives us one minute delay
SWITCH_TIME_DELAY = 1800


class StateMachine:
    "Game state machine"

    def __init__(self, matrix, input):
        "Initializes game machine"
        self.state = "initializing"
        self.matrix = matrix
        self.input = input
        self.game = None
        self.recorder = None
        self.replayer = None
        self.timeout = SWITCH_TIME_DELAY
        self.__update_state__('screen-checker')

    def __new_game__(self):
        "Initialize new game"
        self.game = Game(self.matrix)
        self.recorder = Recorder(self.matrix)

    def __reset_delay__(self):
        self.timeout = SWITCH_TIME_DELAY

    def __delay__(self):
        if self.timeout > 0:
            self.timeout -= 1
            return False
        else:
            self.__reset_delay__()
            return True

    def __update_state__(self, state):
        "Applies given state"
        def __exception__():
            raise Exception('Can\'t transfer from ' + self.state + ' to ' +
                            state)
        if state == "screen-checker":
            if self.state == "initializing":
                self.screen_checker = ScreenChecker(self.matrix)
            else:
                __exception__()
        elif state == "game":
            if self.state == "screen-checker" or \
                    self.state == "game-over" or \
                    self.state == "replay":
                self.__new_game__()
            elif self.state == "game-pause":
                pass
            else:
                __exception__()
        elif state == "game-pause":
            if self.state != "game":
                __exception__()
        elif state == "game-over":
            if self.state != "game":
                __exception__()
            self.__reset_delay__()
            self.recorder.store(self.game.score)
            self.matrix.fill('red')
            i = self.matrix.height - 2
            # Show score
            for _ in range(int(self.game.score / 5)):
                for s in range(5):
                    self.matrix.pixel(s + 3, i, 'green')
                i -= 1
            for s in range(self.game.score % 5):
                self.matrix.pixel(s + 3, i, 'green')
            self.matrix.display()
        elif state == "replay":
            if self.state != "game-over" and self.state != "screen-checker":
                __exception__()
            self.replayer = Replayer(self.matrix)
        else:
            __exception__()
        self.state = state

    def tick(self):
        "Do tick"
        inpt = self.input.check()
        if self.state == "screen-checker":
            if inpt['start']:
                self.__update_state__('game')
            if inpt['select']:
                self.__update_state__('replay')
            else:
                self.screen_checker.tick()
        elif self.state == "game":
            # Note: This records previous tick output but that doens't matter
            # as loosing latest frame is harmless
            self.recorder.tick()
            if inpt['start']:
                self.__update_state__('game-pause')
            elif not self.game.tick(inpt):
                self.__update_state__('game-over')
        elif self.state == "game-pause":
            if inpt['start']:
                self.__update_state__('game')
            elif inpt['select']:
                self.__new_game__()
                self.__update_state__('game')
        elif self.state == "game-over":
            if inpt['start']:
                self.__update_state__('game')
            elif self.__delay__():
                self.__update_state__('replay')
        elif self.state == "replay":
            if inpt['start']:
                self.__update_state__('game')
            elif not self.replayer.tick():
                self.replayer = Replayer(self.matrix)
        else:
            raise Exception('Invalid state ' + self.state)
