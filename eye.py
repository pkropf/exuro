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
import math


config = ConfigParser.RawConfigParser()
config.read('exuro.cfg')

_debug = config.getboolean('general', 'debug')
_port  = config.get('arduino', 'port')

_lhpin = config.getint('eye', 'left_horizontal')
_lvpin = config.getint('eye', 'left_vertical')
_rhpin = config.getint('eye', 'right_horizontal')
_rvpin = config.getint('eye', 'right_vertical')

_offset = config.getfloat('eye', 'offset')
_height = config.getfloat('eye', 'height')

_kinect_x = float(config.getint('kinect', 'x'))
_kinect_y = float(config.getint('kinect', 'y'))
_kinect_hfield = config.getint('kinect', 'hfield')
_kinect_vfield = config.getint('kinect', 'vfield')


class Eye(object):
    def __init__(self, name, horizontal_pin, vertical_pin, port, offset, height=_height):
        self.name = name
        self.hpin = horizontal_pin
        self.vpin = vertical_pin
        self.port = port
        self.hservo = Servo(self.hpin, port)
        self.vservo = Servo(self.vpin, port)
        self.offset = offset
        self.height = height

        if _debug:
            print self.name, self.hpin, self.vpin, self.port, self.offset
            print self.hservo
            print self.vservo


    def str(self):
        return self.name


    def move(self, horizontal, vertical):
        if _debug:
            print 'move', self.name, 'to', horizontal, vertical
        self.hservo.send(horizontal)
        self.vservo.send(vertical)


    def focus(self, distance, point):
        """distance in meters.
        point is x, y tuple for location in grid space.
        
        angle of focus for x axis is x % of _kinect_x % of _kinect_hfield
        angle of focus for y axis is y % of _kinect_y % of _kinect_vfield
        """
        x = point[0] / _kinect_x * _kinect_hfield
        y = point[1] / _kinect_y * _kinect_vfield
        print distance, point, x, y


Left  = Eye('left eye',  _lhpin, _lvpin, _port, -_offset)
Right = Eye('right eye', _rhpin, _rvpin, _port, _offset)


def random_eyes():
    from random import Random

    hrange = (10, 160)
    vrange = (40, 160)
    r = Random()

    for x in range(100000):
        Left.move(r.randrange(*hrange), r.randrange(*vrange))
        Right.move(r.randrange(*hrange), r.randrange(*vrange))
        sleep(1.25)



def random_focus():
    from random import Random

    hrange = (0, _kinect_x -1)
    vrange = (0, _kinect_y - 1)
    drange = (0, 3000)
    r = Random()

    for dummy in range(100000):
        h = r.randrange(*hrange)
        v = r.randrange(*vrange)
        d = r.randrange(*drange) / 1000.0
        Left.focus(d, (h, v))
        Right.focus(d, (h, v))
        sleep(0.25)


if __name__ == '__main__':
    #random_eyes()
    random_focus()
