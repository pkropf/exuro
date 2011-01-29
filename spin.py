#! /usr/bin/env python

from commands import Servo
from time import sleep
from eye import LeftEye, RightEye

for z in range(3):
    for x in range(0, 180, 10):
        LeftEye.move(x, 180-x)
        RightEye.move(180-x, x)

    LeftEye.move(0, 180)
    RightEye.move(180, 0)
    sleep(1)
