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
import copy
import pickle

cv.NamedWindow('Depth')
cv.NamedWindow('Video')
print('Press ESC in window to stop')


def get_depth():
    return depth


def get_video():
    return video


while 1:
    depth, timestamp = freenect.sync_get_depth()
    video, timestemp = freenect.sync_get_video()

    cdepth = frame_convert.pretty_depth_cv(copy.deepcopy(depth))
    video = frame_convert.video_cv(video)

    cv.ShowImage('Depth', cdepth)
    cv.ShowImage('Video', video)

    key = cv.WaitKey(10)
    if key == 27:    # escape
        break

    elif key == 115: # lower case s
        print 'scraping a new depth at', timestamp
        pickle.dump(depth, open('depth.pickle', 'w'))
        cv.SaveImage('depth.jpg', video)
