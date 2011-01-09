#!/usr/bin/env python

# hacked by Peter Kropf (pkropf@gmail.com)

# based on the code from http://principialabs.com/arduino-python-4-axis-servo-control/

# originally:
# Created:  23 December 2009
# Author:   Brian D. Wendt (http://principialabs.com/)
# Version:  1.0
# License:  GPLv3 (http://www.fsf.org/licensing/)


import serial
import time


class Command(object):
    def __init__(self, command, pin, port):
        self.command    = command
        self.pin        = pin
        self.port       = port
        self.serial     = None
        self.last_reset = 0

        self.reset_serial()


    def reset_serial(self):
        self.serial = serial.Serial(self.port, 9600, timeout=1)
        self.last_reset = time.time()
        #print self.serial, self.last_reset


    def send(self, parm):
        try:
            duration = time.time() - self.last_reset # it takes around 2 seconds for the arduino be become ready after
            if duration < 2:                         # serial communications have been established. so make sure it's
                time.sleep(2 - duration)             # been at least 2 seconds before the last reset.

            self.serial.write(chr(255))          # header, start of a new command set
            self.serial.write(chr(self.command)) # with our command code
            self.serial.write(chr(self.pin))     # connected to pin
            self.serial.write(chr(parm))         # with this parameter

        except serial.serialutil.SerialException:
            self.reset_serial()



class Blink(Command):
    def __init__(self, pin, port):
        super(Blink, self).__init__(0, pin, port) 


class Servo(Command):
    def __init__(self, pin, port):
        super(Servo, self).__init__(1, pin, port)
