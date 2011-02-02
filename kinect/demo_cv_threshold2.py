#!/usr/bin/env python
# -*- coding: utf-8 -*-

import freenect
import cv
import frame_convert
import numpy as np


threshold = 30
current_depth = 750
closest = (1,1)

def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def show_depth():
    global threshold
    global current_depth
    global closest

    depth, timestamp = freenect.sync_get_depth()
    depthm = np.ma.masked_values(depth, 2047)
    amin = depthm.argmin()
    y = amin / depthm.shape[1]
    x = amin - (y * depthm.shape[1])
    closest = (x, y)

    print closest
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
    cv.Circle(video, closest, 4, (0, 255, 0))
    cv.ShowImage('Video', video)


cv.NamedWindow('Depth')
cv.NamedWindow('Video')
cv.CreateTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv.CreateTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')


while 1:
    show_depth()
    show_video()
    if cv.WaitKey(5) == 27:
        break
