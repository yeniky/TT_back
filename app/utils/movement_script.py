import random
import requests
import decimal
from time import sleep
from datetime import datetime
import numpy as np

# curl --data "POS,0,ABCD,100,150,0.6,50,xE5" https://localhost:5000/api/positions


def build_path():

    # -2.1419152135663904	-0.488385021559953	1.0607879462723506	2.387408714715984

    line1 = [[x, -0.488385021559953]
             for x in np.linspace(-2.1419152135663904, 1.0607879462723506, num=8, endpoint=False)]
    line2 = [[1.0607879462723506, y]
             for y in np.linspace(-0.488385021559953, 2.387408714715984, num=8, endpoint=False)]
    line3 = [[x, 2.387408714715984]
             for x in np.linspace(1.0607879462723506, -2.1419152135663904, num=8, endpoint=False)]
    line4 = [[-2.1419152135663904, y]
             for y in np.linspace(2.387408714715984, -0.488385021559953, num=8)]
    return line1+line2+line3+line4


def generate_positions(positions):
    for x in positions:
        pos = create_pos('alpha', x[0], x[1])
        print(pos)
        requests.post('http://127.0.0.1:5000/api/positions', data=pos)
        sleep(1)


def create_pos(address, x, y):
    return f"POS,0,{address},{x},{y},{0}.6,50,xE5"


path = build_path()
print([x[0] for x in path])
print([x[1] for x in path])
while(True):
    generate_positions(path)
    sleep(60)
