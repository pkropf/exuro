#!/usr/bin/env python

# hacked by Peter Kropf (pkropf@gmail.com)

# based on the code from http://principialabs.com/arduino-python-4-axis-servo-control/

# originally:
# Created:  23 December 2009
# Author:   Brian D. Wendt (http://principialabs.com/)
# Version:  1.0
# License:  GPLv3 (http://www.fsf.org/licensing/)

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


import serial
import time
import cfg


class cmd(object):
    blink           = 0  # blink an led
    servo           = 1  # move a servo
    register_switch = 2  # register a switch on a pin
    read_switch     = 3  # read the status of a switch, open / closed
    pin             = 4  # set a pin to the specified voltage


class Command(object):
    def __init__(self, command, pin, port):
        self.command      = command
        self.pin          = pin
        self.port         = port
        self.serial       = None
        self.last_reset   = 0
        self.check_msg    = None

        self.reset_serial()


    def reset_serial(self):
        self.serial = serial.Serial(self.port, cfg.arduino.baud, timeout=1)
        # todo: last_reset should be a singeton across the same self.port
        self.last_reset = time.time()
        #print self.serial, self.last_reset


    def send(self, parm):
        if not self.check(parm):
            raise ValueError, (parm, self.check_msg)

        try:
            duration = time.time() - self.last_reset # it takes around 2 seconds for the arduino be become ready after
            if duration < cfg.arduino.reset_time:            # serial communications have been established. so make sure it's
                time.sleep(cfg.arduino.reset_time - duration)# been at least 2 seconds before the last reset.

            self.serial.write(chr(255))          # header, start of a new command set
            self.serial.write(chr(self.command)) # with our command code
            self.serial.write(chr(self.pin))     # connected to pin
            self.serial.write(chr(parm))         # with this parameter
            self.last_message = time.time()

        except serial.serialutil.SerialException:
            time.sleep(cfg.arduino.reset_time)
            self.reset_serial()

    def check(self, parm):
        return True



class Blink(Command):
    def __init__(self, pin, port):
        super(Blink, self).__init__(cmd.blink, pin, port) 



class Servo(Command):
    def __init__(self, pin, min, max, port, pause = cfg.servo.pause):
        super(Servo, self).__init__(cmd.servo, pin, port)
        self.min          = min
        self.max          = max
        self.check_msg    = 'Servo angle must be an integer between %d and %d.' % (self.min, self.max)
        self.last_message = 0      # when the last message was sent
        self.pause        = pause  # how long to wait before sending the next servo


    def send(self, parm):
        duration = time.time() - self.last_message
        if duration < self.pause:
            time.sleep(self.pause - duration)

        super(Servo, self).send(parm)


    def check(self, parm):
        return self.min <= parm <= self.max



class Pin(Command):
    def __init__(self, pin, port):
        super(Pin, self).__init__(cmd.pin, pin, port)
