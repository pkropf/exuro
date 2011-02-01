#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
