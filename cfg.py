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


import ConfigParser


config = ConfigParser.RawConfigParser()
config.read('exuro.cfg')


class servo(object):
    pause      = config.getfloat('servo',   'pause')


class arduino(object):
    reset_time = config.getfloat('arduino', 'reset_time')
    baud       = config.getint('arduino',   'baud')
    port       = config.get('arduino', 'port')


class general(object):
    debug = config.getboolean('general', 'debug')


class eye(object):

    class left(object):
        hpin = config.getint('left eye', 'horizontal')
        vpin = config.getint('left eye', 'vertical')
        hmin = config.getint('left eye', 'hmin')
        hmax = config.getint('left eye', 'hmax')
        horient = config.getint('left eye', 'horient')
        vmin = config.getint('left eye', 'vmin')
        vmax = config.getint('left eye', 'vmax')
        vorient = config.getint('left eye', 'vorient')

        offset = config.getfloat('left eye', 'offset')
        height = config.getfloat('left eye', 'height')

    class right(object):
        hpin = config.getint('right eye', 'horizontal')
        vpin = config.getint('right eye', 'vertical')
        hmin = config.getint('right eye', 'hmin')
        hmax = config.getint('right eye', 'hmax')
        horient = config.getint('right eye', 'horient')
        vmin = config.getint('right eye', 'vmin')
        vmax = config.getint('right eye', 'vmax')
        vorient = config.getint('right eye', 'vorient')

        offset = config.getfloat('right eye', 'offset')
        height = config.getfloat('right eye', 'height')


class kinect(object):
    height  = config.getfloat('kinect', 'height')
    x       = config.getint('kinect', 'x')
    y       = config.getint('kinect', 'y')
    hfield  = config.getint('kinect', 'hfield')
    vfield  = config.getint('kinect', 'vfield')
