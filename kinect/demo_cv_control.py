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

import freenect
import cv
import frame_convert
import numpy as np


threshold = 100
current_depth = 0
kill_me = False


def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def depth(dev, data, timestamp):
    global threshold, current_depth, kill_me

    depth = 255 * np.logical_and(data >= current_depth - threshold,
                                 data <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 1)
    cv.SetData(image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
    cv.ShowImage('Depth', image)

    key = cv.WaitKey(10)
    if key == 27:
        kill_me = True


def video(dev, data, timestamp):
    global kill_me

    cv.ShowImage('Video', frame_convert.video_cv(data))
    key = cv.WaitKey(10)
    if key == 27:
        kill_me = True


cv.NamedWindow('Depth')
cv.NamedWindow('Video')
cv.CreateTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv.CreateTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')


def body(dev, ctx):
    global kill_me

    if kill_me:
        raise freenect.Kill


freenect.runloop(depth = depth,
                 video = video,
                 body  = body)
