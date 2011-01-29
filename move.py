#! /usr/bin/env python


from commands import Servo
from time import sleep
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('exuro.cfg')

port  = config.get('arduino', 'port')
s1pin = config.getint('arduino', 'left_eye_horizontal')
s2pin = config.getint('arduino', 'left_eye_vertical')
s3pin = config.getint('arduino', 'right_eye_horizontal')
s4pin = config.getint('arduino', 'right_eye_vertical')
a1  = 10
a2  = 170

s1 = Servo(s1pin, port)
s2 = Servo(s2pin, port)

for s, a in [(s1, 10), (s2, 10), (s1, 170), (s2, 170), (s1, 86), (s2, 86),]:
    print 'moving servo on pin %d to %d' % (s.pin, a)
    s.send(a)
    sleep(1)
