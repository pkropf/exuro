#! /usr/bin/env python


import serial
from time import sleep


pin = 13
count = 10
port = '/dev/tty.usbmodemfa141'

serial = serial.Serial(port, 9600, timeout=1)
sleep(2)

serial.write(chr(255))
serial.write(chr(0))
serial.write(chr(pin))
serial.write(chr(count))
sleep(count * 2)
