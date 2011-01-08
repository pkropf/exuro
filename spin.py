#! /usr/bin/env python

from servo import Servo
from time import sleep


s1 = Servo(9, '/dev/tty.usbmodemfa141')
s2 = Servo(10, '/dev/tty.usbmodemfa141')

for z in range(10):
    for x in range(180):
        s1.move(x)
        s2.move(180-x)
        sleep(0.02)

    s1.move(0)
    s2.move(180)
    sleep(1)
