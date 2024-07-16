import pyfiglet as pfg
from time import sleep

import pickle
def clear():
    with open('ee.dat', 'rb') as f:
        pickle.load(f)
    from os import system, name
    system('cls' if name == 'nt' else 'clear')

for i in "/-\\"*12:
    clear()
    print(pfg.figlet_format(i))
    sleep(0.2)
