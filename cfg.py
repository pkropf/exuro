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


exuro = ConfigParser.RawConfigParser()
exuro.read('exuro.cfg')
exuro.read('exuro_local.cfg') # override any values in the general configuration file


class servo(object):
    pause       = exuro.getfloat('servo',   'pause')
    limit_watch = exuro.getboolean('servo', 'limit_watch')


class arduino(object):
    reset_time = exuro.getfloat('arduino', 'reset_time')
    baud       = exuro.getint('arduino',   'baud')
    port       = exuro.get('arduino', 'port')


class general(object):
    debug = exuro.getboolean('general', 'debug')


class eye(object):

    class left(object):
        active = exuro.getboolean('left eye', 'active')
        hpin = exuro.getint('left eye', 'horizontal')
        vpin = exuro.getint('left eye', 'vertical')
        hmin = exuro.getint('left eye', 'hmin')
        hmax = exuro.getint('left eye', 'hmax')
        horient = exuro.getint('left eye', 'horient')
        vmin = exuro.getint('left eye', 'vmin')
        vmax = exuro.getint('left eye', 'vmax')
        vorient = exuro.getint('left eye', 'vorient')

        offset = exuro.getfloat('left eye', 'offset')
        height = exuro.getfloat('left eye', 'height')

    class right(object):
        active = exuro.getboolean('right eye', 'active')
        hpin = exuro.getint('right eye', 'horizontal')
        vpin = exuro.getint('right eye', 'vertical')
        hmin = exuro.getint('right eye', 'hmin')
        hmax = exuro.getint('right eye', 'hmax')
        horient = exuro.getint('right eye', 'horient')
        vmin = exuro.getint('right eye', 'vmin')
        vmax = exuro.getint('right eye', 'vmax')
        vorient = exuro.getint('right eye', 'vorient')

        offset = exuro.getfloat('right eye', 'offset')
        height = exuro.getfloat('right eye', 'height')


class kinect(object):
    height  = exuro.getfloat('kinect', 'height')
    x       = exuro.getint('kinect', 'x')
    y       = exuro.getint('kinect', 'y')
    hfield  = exuro.getint('kinect', 'hfield')
    vfield  = exuro.getint('kinect', 'vfield')


class keys(object):
    consumer_key    = exuro.get('keys', 'consumer_key')
    consumer_secret = exuro.get('keys', 'consumer_secret')
    access_key      = exuro.get('keys', 'access_key')
    access_secret   = exuro.get('keys', 'access_secret')
