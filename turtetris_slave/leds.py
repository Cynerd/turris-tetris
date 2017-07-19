from subprocess import call


def prepare():
    "Prepare leds"
    call("rainbow all enable FFFFFF", shell=True)


def clear():
    "Clear previous changes"
    call("rainbow all auto", shell=True)


__MAP__ = [
    'pwr',
    'lan0',
    'lan1',
    'lan2',
    'lan3',
    'lan4',
    'wan',
    'pci1',
    'pci2',
    'pci3',
    'usr1',
    'usr2'
]


def output(data):
    "Output received data to leds"
    args = ['rainbow']
    for i in range(0, 12):
        args.append(__MAP__[i])
        args.append(str(data[i]))
    call(args)
