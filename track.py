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
import math
import eye
import cfg


threshold     = 30                           # 
current_depth = 750                          # 
closest       = (1,1)                        # the closest location
distance      = 1.0                          # distance in meters from the kinect
shape         = (cfg.kinect.y, cfg.kinect.x) # assumed shape of the depth array


def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def move_eyes():
    """
    """
    global closest, distance
    eye.Left.focus(distance, (closest[1], closest[0]))
    eye.Right.focus(distance, (closest[1], closest[0]))


def show_depth():
    global threshold, current_depth, closest, distance

    depth, timestamp = freenect.sync_get_depth()
    depthm = np.ma.masked_values(depth, 2047)
    depthm = depth
    amin = depthm.argmin()
    closest = np.unravel_index(amin, depthm.shape)

    distance = 0.1236 * math.tan(depthm.flatten()[amin] / 2842.5 + 1.1863)
    #print 'depth:', closest, amin, depthm.flatten()[amin], distance
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 1)
    cv.SetData(image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
    cv.ShowImage('Depth', image)


def show_video():
    video = frame_convert.video_cv(freenect.sync_get_video()[0])
    cv.Circle(video, (closest[1], closest[0]), 8, (0, 0, 255))
    cv.Circle(video, (closest[1], closest[0]), 4, (0, 0, 255))
    cv.ShowImage('Video', video)


cv.NamedWindow('Depth')
cv.NamedWindow('Video')
cv.CreateTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv.CreateTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')


while 1:
    show_depth()
    show_video()
    move_eyes()

    if cv.WaitKey(5) == 27:
        break
