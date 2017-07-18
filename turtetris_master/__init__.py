from .usb_input import Gamepad


def main():
    "Main function"
    inpt = Gamepad()
    while True:
        print(inpt.check())


if __name__ == '__main__':
    main()
