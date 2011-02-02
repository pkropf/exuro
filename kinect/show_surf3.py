#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import cv
import frame_convert
import copy
import pickle
import time


_hessian     = 2000
hessian_max  = 20000
_octive      = 4
octive_max   = 25
_layer       = 0
layer_max    = 25
changed      = True


def change_hessian(value):
    global _hessian, changed
    _hessian = value
    changed = True

def change_octive(value):
    global _octive, changed
    _octive = value
    changed = True

def change_layer(value):
    global _layer, changed
    _layer = value
    changed = True

#cv.NamedWindow('Depth')
cv.NamedWindow('Processed')
cv.NamedWindow('Gray')
cv.CreateTrackbar('hessian',  'Processed', _hessian,  hessian_max,  change_hessian)
cv.CreateTrackbar('octive',   'Processed', _octive,   octive_max,   change_octive)
cv.CreateTrackbar('layer',    'Processed', _layer,    layer_max,    change_layer)

#depth = pickle.load(open('depth.pickle', 'r'))
video = cv.LoadImageM('depth.jpg')
gray_base = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
gray_show = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(video, gray_base, cv.CV_RGB2GRAY)
cv.ShowImage('Gray', gray_base)

while 1:
    if changed:
        changed = False

        cv.Canny(gray_base, gray_show, 50, 180)
        (keypoints, descriptors) = cv.ExtractSURF(gray_show, None, cv.CreateMemStorage(), (0, _hessian + 1, _octive + 1, _layer + 1))

        print len(keypoints)
        for ((x, y), laplacian, size, dir, hessian) in keypoints:
            #print "x=%d y=%d laplacian=%d size=%d dir=%f hessian=%f" % (x, y, laplacian, size, dir, hessian)
            radio = size*1.2/9.*2
            #print "radioOld: ", int(radio)
            color = (255, 0, 0)
            if radio < 3:
                radio = 2
                color = cv.Scalar(0, 255, 0)
            #print "radioNew: ", int(radio)
            cv.Circle(gray_show, (int(x), int(y)), int(size), color)

        cv.ShowImage('Processed', gray_show)

    key = cv.WaitKey(10)
    if key == 27:    # escape
        break
