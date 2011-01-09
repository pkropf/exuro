#! /usr/bin/env python


from commands import Servo
from time import sleep


pin1 = 9
pin2 = 10
a1  = 10
a2  = 170

s1 = Servo(pin1, '/dev/tty.usbmodemfa141')
s2 = Servo(pin2, '/dev/tty.usbmodemfa141')
sleep(2)

for s, a in [(s1, 10), (s2, 10), (s1, 170), (s2, 170), (s1, 86), (s2, 86),]:
    print 'moving servo on pin %d to %d' % (s.pin, a)
    s.move(a)
    sleep(1)
