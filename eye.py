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
import cfg
from time import sleep
import math


class Eye(object):
    def __init__(self, name, active,
                 horizontal_pin, vertical_pin, 
                 hmin, hmax, vmin, vmax,
                 port, offset, 
                 height,
                 horient, vorient):
        self.name = name
        self.active = active
        self.hpin = horizontal_pin
        self.vpin = vertical_pin
        self.hmin = hmin
        self.hmax = hmax
        self.vmin = vmin
        self.vmax = vmax
        self.port = port

        if self.active:
            self.hservo = Servo(self.hpin, self.hmin, self.hmax, port)
            self.vservo = Servo(self.vpin, self.vmin, self.vmax, port)
        else:
            self.hservo = None
            self.vservo = None

        self.offset = offset
        self.height = height
        self.horient = horient
        self.vorient = vorient
        self.move(*self.center())
        self.focus = self.focus_simple
        #self.focus = self.focus_angles

        if cfg.general.debug:
            print self.name, self.hpin, self.vpin, self.port, self.offset
            print self.hservo
            print self.vservo


    def __unicode__(self):
        return self.name


    def settings(self):
        print 'name:',    self.name
        print 'active:',  self.active
        print 'hpin:',    self.hpin
        print 'vpin:',    self.vpin
        print 'hmin:',    self.hmin
        print 'hmax:',    self.hmax
        print 'vmin:',    self.vmin
        print 'vmax:',    self.vmax
        print 'port:',    self.port
        print 'hservo:',  self.hservo
        print 'vservo:',  self.vservo
        print 'offset:',  self.offset
        print 'height:',  self.height
        print 'horient:', self.horient
        print 'vorient:', self.vorient


    def center(self):
        return self.hmin + ((self.hmax - self.hmin) / 2.0), self.vmin + ((self.vmax - self.vmin) / 2.0)


    def move(self, horizontal, vertical):
        if self.active:
            self.hservo.send(horizontal)
            self.vservo.send(vertical)


    def focus_simple(self, distance, point):
        """distance in meters.
        point is x, y tuple for location in grid space.

        angle of focus is currently very simplistic. it doesn't yet
        take into account that the eyes are offset from the center and
        it doesn't yet take into account the distance of the point in
        question.

        calculating the angle of focus depends on how the servo is
        oriented and moves. if a low value moves the servo to the left
        or up, then the calculation is:

            range of movement * percentage of x as related to the
            scale of the axis

        if a high value moves the servo to the left or up, then the
        calculation is:

            axis max - range of movement * percentage of x as related
            to scale of the axis
        """

        xpercent = (self.hmax - self.hmin) * (point[0] / float(cfg.kinect.x))
        ypercent = (self.vmax - self.vmin) * (point[1] / float(cfg.kinect.y))

        if self.horient == 1:                # movement scale goes from high to low
            x = self.hmin + xpercent
        else:                                # movement scale goes from low to high
            x = self.hmax - xpercent


        if self.vorient == 1:                # movement scale goes from high to low
            y = self.vmin + ypercent
        else:                                # movement scale goes from low to high
            y = self.vmax - ypercent

        if cfg.general.debug:
            print self.name, distance, point, x, y

        self.move(x, y)


    def focus_angles(self, distance, point):
        """distance in meters.
        point is x, y tuple for location in grid space.

        to calculate the focus for an eye on the x axis:

            1) calculate the distance of the known point (px, py) to the center (cx, cy):

                 radius = sqrt(((px - cx) ** 2) + ((py - cy) ** 2))

                 where:

                     cx, cy = 640 / 2, 480 / 2

            2) calculate the distance in pixels from the kinect to the center of the 
               640x480 field:

                 x_to_center = 320 / tan(kinect_field_x / 2)

                 where:
                     320 is 1/2 of the horizontal field (sets up for a right triangle)
                     kinect_field_x is the kinect's field of vision along the x axis.

            3) x_angle = atan(radius / x_to_center)

        for the y axis:

            1) same as for x axis

            2) y_to_center = 240 / tan(kinect_field_y / 2)

                where 240 is 1/2 of the vertical field and kinect_field_y is the kinect's
                field of vision along the y axis.

            3) y_angle = atan(radius / y_to_center)
        """

        radius = math.sqrt(((point[0] - 320) ** 2) + ((point[1] - 240) ** 2))

        x_to_center = 320 / math.tan(math.radians(cfg.kinect.x / 2))
        x_angle = math.degrees(math.atan(radius / x_to_center))

        y_to_center = 240 / math.tan(math.radians(cfg.kinect.y / 2))
        y_angle = math.degrees(math.atan(radius / y_to_center))

        if self.horient == 1:                # movement scale goes from high to low
            x = 90 - x_angle
        else:                                # movement scale goes from low to high
            x = 90 + x_angle


        if self.vorient == 1:                # movement scale goes from high to low
            y = 90 - y_angle
        else:                                # movement scale goes from low to high
            y = 90 + y_angle

        if cfg.general.debug:
            print distance, point, x, y, radius, x_angle, y_angle, self.horient

        self.move(x, y)


Left  = Eye('left eye', cfg.eye.left.active,
            cfg.eye.left.hpin, cfg.eye.left.vpin,
            cfg.eye.left.hmin, cfg.eye.left.hmax, 
            cfg.eye.left.vmin, cfg.eye.left.vmax,
            cfg.arduino.port, 
            cfg.eye.left.offset, cfg.eye.left.height,
            cfg.eye.left.horient, cfg.eye.left.vorient)

Right = Eye('right eye', cfg.eye.right.active,
            cfg.eye.right.hpin, cfg.eye.right.vpin, 
            cfg.eye.right.hmin, cfg.eye.right.hmax, 
            cfg.eye.right.vmin, cfg.eye.right.vmax,
            cfg.arduino.port,
            cfg.eye.right.offset, cfg.eye.right.height,
            cfg.eye.right.horient, cfg.eye.right.vorient)


def random_eyes():
    from random import Random

    r = Random()

    for x in range(100000):
        Left.move(r.randrange(cfg.eye.left.hmin, cfg.eye.left.hmax), 
                  r.randrange(cfg.eye.left.vmin, cfg.eye.left.vmax))

        Right.move(r.randrange(cfg.eye.right.hmin, cfg.eye.right.hmax),
                   r.randrange(cfg.eye.right.vmin, cfg.eye.right.vmax))
        sleep(0.25)



def random_focus():
    from random import Random

    hrange = (0, cfg.kinect.x - 1)
    vrange = (0, cfg.kinect.y - 1)
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
    random_eyes()
    #random_focus()
