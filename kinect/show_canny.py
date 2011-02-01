#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
