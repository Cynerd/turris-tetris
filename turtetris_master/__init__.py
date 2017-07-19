import time
from .led_output import Matrix
from .usb_input import Gamepad
from .state_machine import StateMachine


def main():
    "Main function"
    inpt = Gamepad()
    mtrx = Matrix()
    sm = StateMachine(mtrx, inpt)
    while True:
        tstart = time.time()
        sm.tick()
        trest = (1/60) - (time.time() - tstart)
        if trest > 0:
            time.sleep(trest)
        else:
            print("Output took too long!!")


if __name__ == '__main__':
    main()
