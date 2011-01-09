#! /usr/bin/env python


from servo import Servo
from time import sleep


s1 = Servo(9, '/dev/tty.usbmodemfa141')

s1.move(10)
s1.move(170)
sleep(1)
