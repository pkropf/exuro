#!/usr/bin/env python
# -*- coding: utf-8 -*-

import freenect
import cv
import frame_convert
import numpy as np


threshold = 30
current_depth = 750


def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def show_depth():
    global threshold
    global current_depth

    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 1)
    cv.SetData(image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
    cv.ShowImage('Depth', image)

    print 'depth:', type(depth), dir(depth)
    print ''

    print 'image:', type(image), dir(image)
    print ''

    x = cv.CreateMat(image.height, image.width, cv.IPL_DEPTH_8U)
    cv.Convert(image, x)

    smaller = cv.CreateMat(image.height / 10, image.width / 10, cv.IPL_DEPTH_8U)
    print 'smaller:', type(smaller), dir(smaller)
    print ''

    cv.Resize(image, smaller)
    cv.ShowImage('Reduced', smaller)


def show_video():
    cv.ShowImage('Video', frame_convert.video_cv(freenect.sync_get_video()[0]))


cv.NamedWindow('Depth')
cv.NamedWindow('Video')
cv.NamedWindow('Reduced')
cv.CreateTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv.CreateTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')


while 1:
    show_depth()
    show_video()
    if cv.WaitKey(5) == 27:
        break
