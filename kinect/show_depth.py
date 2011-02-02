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

cv.NamedWindow('Depth')
depth = pickle.load(open('depth.pickle', 'r'))

def get_depth():
    return frame_convert.pretty_depth_cv(copy.deepcopy(depth))

def clicked(event, col, row, flags, param):
    if event == cv.CV_EVENT_MOUSEMOVE:
        pass
    elif event == cv.CV_EVENT_LBUTTONDOWN:
        print 'r:', row, 'c:', col, 'd:', depth[row][col]

cv.SetMouseCallback('Depth', clicked, None)

while 1:
    cv.ShowImage('Depth', get_depth())

    key = cv.WaitKey(10)
    if key == 27:    # escape
        break
