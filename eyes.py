#! /usr/bin/env python


from commands import Servo
from eye import Eye
from time import sleep


from random import Random

lvpin = 9
lhpin = 10
rvpin = 11
rhpin = 12
hrange = (10, 160)
vrange = (40, 160)
port = '/dev/tty.usbmodemfd131'
leye = Eye(lhpin, lvpin, port)
reye = Eye(rhpin, rvpin, port)
r = Random()

for x in range(100000):
    leye.move(r.randrange(*hrange), r.randrange(*vrange))
    reye.move(r.randrange(*hrange), r.randrange(*vrange))
    sleep(0.5)
