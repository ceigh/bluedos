import subprocess

"""def wait(msg):  # Loading animation
    from threading import Thread
    def animation(m):
        from time import sleep
        from itertools import cycle
        for c in cycle('-/|\\'):
            print("%s %s\r" % (m, c), flush=True, end='')
            sleep(0.2)
    Thread(target=animation, args=(msg,), daemon=True).start()"""


def confirm(question):
    while 1:
        reply = input("%s (y/n): " % question).lower()
        if reply == 'n':
            return 0
        elif reply in ('y', ''):
            return 1


def get_devices():
    print("Scanning...")
    hcitool_out = subprocess.check_output(['hcitool', 'scan']).decode()[13:-1]
    devices = [i.split('\t')[1:] for i in hcitool_out.split('\n') if len(hcitool_out) != 0]
    return devices


def main():
    devices = get_devices()
    dev_number = len(devices)
    if dev_number == 0:
        print("\nNo devices around")
        if confirm("Want to try again?"):
            main()
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
    print("\tDone.")


print("\tBluedos 0.2 by @ceigh\n")
main()
