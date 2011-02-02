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


_low     = 200
low_max  = 1000
_high    = 400
high_max = 1000
changed      = True

def change_low(value):
    global _low, changed
    _low = value
    changed = True

def change_high(value):
    global _high, changed
    _high = value
    changed = True

#cv.NamedWindow('Depth')
cv.NamedWindow('Processed')
cv.NamedWindow('Gray')
cv.CreateTrackbar('low',  'Processed', _low,  low_max,  change_low)
cv.CreateTrackbar('high', 'Processed', _high, high_max, change_high)

#depth = pickle.load(open('depth.pickle', 'r'))
video = cv.LoadImageM('depth.jpg')
gray_base = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
gray_show = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(video, gray_base, cv.CV_RGB2GRAY)
cv.ShowImage('Gray', gray_base)

while 1:
    if changed:
        changed = False

        cv.Canny(gray_base, gray_show, _low, _high)
        cv.ShowImage('Processed', gray_show)

    key = cv.WaitKey(10)
    if key == 27:    # escape
        break
