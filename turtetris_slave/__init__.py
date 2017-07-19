import json
import zmq
from subprocess import check_output
from . import leds


def socket_init(line):
    "Initialize socket for given line"
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.subscribe('line' + str(line))
    # socket.setsockopt_string(zmq.SUBSCRIBE, 'line' + str(line))
    socket.connect('tcp://192.168.2.1:4444')  # TODO change to 192.168.1.1
    return socket


def main():
    "Main function"
    line = int(check_output("uci get turtetris.line", shell=True))
    print("Starting turtetris client and connecting as line " + str(line))
    sck = socket_init(line)
    leds.prepare()
    while True:
        msg = sck.recv_string()
        json0 = msg.find(' ')  # First empty char is end of envelope
        leds.output(json.loads(msg[json0:]))


if __name__ == '__main__':
    main()
