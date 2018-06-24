import subprocess
from itertools import cycle
from threading import Thread
from time import sleep


# Etc
def loop():
    for c in cycle('-/|\\'):
        print('Running ' + c + '\r', flush=True, end='')
        sleep(0.2)


print("Bluedos 0.2 by @ceigh\n")
Thread(target=loop, daemon=True).start()

# Main part
hcitool_out = subprocess.check_output(['hcitool', 'scan']).decode()[13:-1]

data_table = [i.split('\t')[1:] for i in hcitool_out.split('\n')]
print(data_table)
