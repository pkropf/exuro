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
import numpy
import pickle
import taber

depth  = pickle.load(open('depth.pickle', 'r'))
depthx = numpy.ma.masked_values(depth, 2047)
video  = cv.LoadImageM('depth.jpg')
gray   = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(video, gray, cv.CV_RGB2GRAY)

(keypoints, descriptors) = cv.ExtractSURF(gray, None, cv.CreateMemStorage(), (0, 8000, 4, 1))

x = [z[0][0] for z in keypoints]
y = [z[0][1] for z in keypoints]

print gray
print 'min(x):', min(x), 'max(x):', max(x)
print 'min(y):', min(y), 'max(y):', max(y)
