import time
from .led_output import Matrix
from .usb_input import Gamepad
from .screen_checker import ScreenChecker


def main():
    "Main function"
    inpt = Gamepad()
    mtrx = Matrix()
    sc = ScreenChecker(mtrx)
    mtrx.display()  # Display first state
    while True:
        tstart = time.time()
        ##
        #print(inpt.check())
        if sc.tick():
            mtrx.display()
            #print(mtrx.__mat__[2])
        ##
        trest = (1/60) - (time.time() - tstart)
        if trest > 0:
            time.sleep(trest)
        else:
            print("Output took too long!!")


if __name__ == '__main__':
    main()
