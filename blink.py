#! /usr/bin/env python


from commands import Blink
from time import sleep

b = Blink(13, '/dev/tty.usbmodemfa141')
sleep(2)
b.blink(10)
sleep(20)
