import subprocess
from threading import Thread


def wait(msg):
    def animation(m):
        from time import sleep
        from itertools import cycle
        for c in cycle('-/|\\'):
            print("%s %s\r" % (m, c), flush=True, end='')
            sleep(0.2)

    Thread(target=animation, args=(msg,), daemon=True).start()


def get_devices():
    wait("Running")
    hcitool_out = subprocess.check_output(['hcitool', 'scan']).decode()[13:-1]
    devices = [i.split('\t')[1:] for i in hcitool_out.split('\n') if len(hcitool_out) != 0]
    return devices


def attack():
    devices = get_devices()
    dev_number = len(devices)
    if dev_number == 0:
        print("\nNo devices around")
        while 1:
            reply = input("Want to try again? (y/n): ").lower()
            if reply == 'n':
                print("Bye!")
                exit(0)
            elif reply in ('y', ''):
                attack()

    elif dev_number == 1:
        wait("Attacking '%s'" % devices[0][1])
    else:
        print("Multiply des")


print("Bluedos 0.2 by @ceigh\n")
attack()
