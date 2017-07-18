import time
from .led_output import Matrix
from .usb_input import Gamepad


def main():
    "Main function"
    inpt = Gamepad()
    print('Gamepad initialized')
    mtrx = Matrix()
    print('Matrix initialized')
    while True:
        print('loop!!!!')
        print(inpt.check())
        mtrx.display()
        time.sleep(1)


if __name__ == '__main__':
    main()
