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
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('exuro.cfg')

_pause      = config.getfloat('servo',   'pause')
_reset_time = config.getfloat('arduino', 'reset_time')


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
        self.serial = serial.Serial(self.port, 9600, timeout=1)
        self.last_reset = time.time()
        #print self.serial, self.last_reset


    def send(self, parm):
        if not self.check(parm):
            raise ValueError, self.check_msg

        try:
            duration = time.time() - self.last_reset # it takes around 2 seconds for the arduino be become ready after
            if duration < _reset_time:               # serial communications have been established. so make sure it's
                time.sleep(_reset_time - duration)             # been at least 2 seconds before the last reset.

            self.serial.write(chr(255))          # header, start of a new command set
            self.serial.write(chr(self.command)) # with our command code
            self.serial.write(chr(self.pin))     # connected to pin
            self.serial.write(chr(parm))         # with this parameter
            self.last_message = time.time()

        except serial.serialutil.SerialException:
            time.sleep(_reset_time)
            self.reset_serial()

    def check(self, parm):
        return True



class Blink(Command):
    def __init__(self, pin, port):
        super(Blink, self).__init__(0, pin, port) 



class Servo(Command):
    def __init__(self, pin, port, pause = _pause):
        super(Servo, self).__init__(1, pin, port)
        self.check_msg    = 'Servo angle must be an integer between 0 and 180.'
        self.last_message = 0      # when the last message was sent
        self.pause        = pause  # how long to wait before sending the next servo


    def send(self, parm):
        duration = time.time() - self.last_message
        if duration < self.pause:
            time.sleep(self.pause - duration)

        super(Servo, self).send(parm)


    def check(self, parm):
        return 0 <= parm <= 180



class Pin(Command):
    def __init__(self, pin, port):
        super(Pin, self).__init__(4, pin, port)
