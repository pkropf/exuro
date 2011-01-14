#! /usr/bin/env python


from commands import Servo
from time import sleep




class Eye(object):
    def __init__(self, horizontal_pin, vertical_pin, port):
        self.hpin = horizontal_pin
        self.vpin = vertical_pin
        self.port = port
        self.hservo = Servo(self.hpin, port)
        self.vservo = Servo(self.vpin, port)

        print self.hpin, self.vpin, self.port
        print self.hservo
        print self.vservo


    def move(self, horizontal, vertical):
        print 'move to', horizontal, vertical
        self.hservo.send(horizontal)
        self.vservo.send(vertical)



if __name__ == '__main__':
    from random import Random

    vpin = 9
    hpin = 10
    hrange = (10, 160)
    vrange = (40, 160)
    port = '/dev/tty.usbmodemfd131'
    eye = Eye(hpin, vpin, port)
    r = Random()
    
    for x in range(1000):
        eye.move(r.randrange(*hrange), r.randrange(*vrange))
