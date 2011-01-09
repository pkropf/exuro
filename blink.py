#! /usr/bin/env python


from servo import Servo
from time import sleep


pin = 9
a1  = 10
a2  = 170

s1 = Servo(pin, '/dev/tty.usbmodemfa141')

print 'moving servo on pin %d to %d' % (pin, a1)
s1.move(a1)
sleep(1)

print 'moving servo on pin %d to %d' % (pin, a2)
s1.move(170)
sleep(1)
