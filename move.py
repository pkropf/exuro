#! /usr/bin/env python

# Copyright (c) 2011 Peter Kropf. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from commands import Servo
from time import sleep
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('exuro.cfg')

port  = config.get('arduino', 'port')
s1pin = config.getint('eye', 'left_horizontal')
s2pin = config.getint('eye', 'left_vertical')
s3pin = config.getint('eye', 'right_horizontal')
s4pin = config.getint('eye', 'right_vertical')
a1  = 10
a2  = 170

s1 = Servo(s1pin, port)
s2 = Servo(s2pin, port)

for s, a in [(s1, 10), (s2, 10), (s1, 170), (s2, 170), (s1, 86), (s2, 86),]:
    print 'moving servo on pin %d to %d' % (s.pin, a)
    s.send(a)
    sleep(1)
