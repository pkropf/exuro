#! /usr/bin/env python

from commands import Servo
from time import sleep


s1 = Servo(9, '/dev/tty.usbmodemfa141')
s2 = Servo(10, '/dev/tty.usbmodemfa141')

for z in range(3):
    for x in range(180):
        s1.send(x)
        s2.send(180-x)
        sleep(0.02)

    s1.send(0)
    s2.send(180)
    sleep(1)
