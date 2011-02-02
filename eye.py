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

_port  = config.get('arduino', 'port')
_lhpin = config.getint('eye', 'left_horizontal')
_lvpin = config.getint('eye', 'left_vertical')
_rhpin = config.getint('eye', 'right_horizontal')
_rvpin = config.getint('eye', 'right_vertical')


class Eye(object):
    def __init__(self, name, horizontal_pin, vertical_pin, port):
        self.name = name
        self.hpin = horizontal_pin
        self.vpin = vertical_pin
        self.port = port
        self.hservo = Servo(self.hpin, port)
        self.vservo = Servo(self.vpin, port)

        print self.hpin, self.vpin, self.port
        print self.hservo
        print self.vservo


    def str(self):
        return self.name

    def move(self, horizontal, vertical):
        print 'move', self.name, 'to', horizontal, vertical
        self.hservo.send(horizontal)
        self.vservo.send(vertical)


LeftEye  = Eye('left eye',  _lhpin, _lvpin, _port)
RightEye = Eye('right eye', _rhpin, _rvpin, _port)


if __name__ == '__main__':
    from random import Random

    hrange = (10, 160)
    vrange = (40, 160)
    r = Random()
    
    for x in range(100000):
        LeftEye.move(r.randrange(*hrange), r.randrange(*vrange))
        RightEye.move(r.randrange(*hrange), r.randrange(*vrange))
        sleep(0.25)
