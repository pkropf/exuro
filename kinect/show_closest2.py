#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv
import frame_convert
import copy
import pickle
import time
import distance
import numpy


cv.NamedWindow('Closest')

depth = pickle.load(open('depth.pickle', 'r'))
video = cv.LoadImageM('depth.jpg')

depthm = numpy.ma.masked_values(depth, 2047)
amin = depthm.argmin()
y = amin / depthm.shape[1]
x = amin - (y * depthm.shape[1])

print 'shape:', depth.shape
print 'min:', depthm.min()
print 'argmin:', amin
print 'x:', x
print 'y:', y

cv.Circle(video, (int(x), int(y)), 2, (0, 255, 0))
cv.ShowImage('Closest', video)

while 1:
    key = cv.WaitKey(10)
    if key == 27:    # escape
        break
