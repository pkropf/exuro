#!/usr/bin/env python

# hacked by Peter Kropf (pkropf@gmail.com)

# based on the code from http://principialabs.com/arduino-python-4-axis-servo-control/

# originally:
# Created:  23 December 2009
# Author:   Brian D. Wendt (http://principialabs.com/)
# Version:  1.0
# License:  GPLv3 (http://www.fsf.org/licensing/)


import serial


class Servo(object):
    def __init__(self, pin, port):
        self.pin = pin
        self.port = port
        self.serial = None
        self.setup()

    def setup(self):
        self.serial = serial.Serial(self.port, 9600, timeout=1)
        #print self.serial

    def move(self, angle):
        try:
            if (0 <= angle <= 180):
                self.serial.write(chr(255))         # header, start of a new command set
                self.serial.write(chr(1))           # command to move the servo
                self.serial.write(chr(self.pin))    # connected to pin
                self.serial.write(chr(angle))       # to this angle

            else:
                raise ValueError, "Servo angle must be an integer between 0 and 180."

        except serial.serialutil.SerialException:
            self.setup()
