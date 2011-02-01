#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
