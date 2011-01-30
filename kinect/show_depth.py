#!/usr/bin/env python

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
