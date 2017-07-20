import usb.core
import usb.backend.libusb1
import usb.util

# Personal Communication Systems, Inc. SNES Gamepad
CONF_SNES_GAMEPAD = {
    "idVendor": 0x0810,
    "idProduct": 0xe501,
    "iInterface": 0,
}


class Gamepad:
    "Simple gamepad handle function"

    def __init__(self, conf=CONF_SNES_GAMEPAD):
        "Initializes usb subsystem"
        backend = usb.backend.libusb1.get_backend(find_library=lambda x:
                                                  "/usr/lib/libusb-1.0.so")
        self.dev = usb.core.find(idVendor=conf['idVendor'],
                                 idProduct=conf['idProduct'],
                                 backend=backend)
        if self.dev is None:
            raise ValueError('Device not found')

        if self.dev.is_kernel_driver_active(conf['iInterface']) is True:
            # Detach any kernel driver so it won't interfere with us
            self.dev.detach_kernel_driver(conf['iInterface'])

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.dev.set_configuration()

        # get an endpoint instance
        self.cfg = self.dev.get_active_configuration()
        intf = self.cfg[(0, 0)]

        self.ep = usb.util.find_descriptor(
            intf,
            # match the first IN endpoint
            custom_match=lambda e:
            usb.util.endpoint_direction(e.bEndpointAddress) ==
            usb.util.ENDPOINT_IN
        )
        assert self.ep is not None

        self.state = {}
        for key in ['left', 'right', 'up', 'down', 'select', 'start']:
            self.state[key] = False

    def check(self):
        "Check the input state"
        data = self.dev.read(self.ep.bEndpointAddress,
                             self.ep.wMaxPacketSize*2, 1000).tolist()
        new_state = {
            "left": data[3] < 120 or bool(data[5] & 0x80),
            "right": data[3] > 140 or bool(data[5] & 0x20),
            "up": data[4] < 120 or bool(data[5] & 0x10),
            "down": data[4] > 140 or bool(data[5] & 0x40),
            "select": bool(data[6] & 0x10),
            "start": bool(data[6] & 0x20),
        }
        changed = {}
        for key in ['left', 'right', 'up', 'down', 'select', 'start']:
            changed[key] = new_state[key] and not self.state[key]
        # TODO repeat
        self.state = new_state
        return changed
