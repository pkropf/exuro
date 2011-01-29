#! /usr/bin/env python


from commands import Servo
from eye import LeftEye, RightEye
from time import sleep
from random import Random

hrange = (10, 160)
vrange = (40, 160)
r = Random()

for x in range(100000):
    leye.move(r.randrange(*hrange), r.randrange(*vrange))
    reye.move(r.randrange(*hrange), r.randrange(*vrange))
    sleep(0.5)
