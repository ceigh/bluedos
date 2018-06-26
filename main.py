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
    hcitool_out = subprocess.check_output(['hcitool', 'scan']).decode()[13:-1]
    devices = [i.split('\t')[1:] for i in hcitool_out.split('\n') if len(hcitool_out) != 0]
    return devices


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
        print("Attacking '%s'..." % devices[0][1])
    else:
        print("Several devices found:")
        for dev in range(dev_number):
            print("%d) '%s' <%s>" % (dev, devices[dev][1], devices[dev][0]))
        while 1:
            try:
                target = int(input("Select a device (0-%d): " % (dev_number - 1)))
            except ValueError:
                continue
            if target in range(dev_number):
                break
        print("Attacking '%s'..." % devices[target][1])


main()
