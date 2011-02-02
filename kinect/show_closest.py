#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv
import frame_convert
import copy
import pickle
import time
import distance


_hessian     = 8000
hessian_max  = 10000
_octive      = 4
octive_max   = 25
_layer       = 0
layer_max    = 25
changed      = True

def change_hessian(value):
    global _hessian, changed
    _hessian = value
    changed = True

def change_octive(value):
    global _octive, changed
    _octive = value
    changed = True

def change_layer(value):
    global _layer, changed
    _layer = value
    changed = True

#cv.NamedWindow('Depth')
cv.NamedWindow('Processed')
#cv.NamedWindow('Gray')
cv.NamedWindow('Closest')
cv.CreateTrackbar('hessian',  'Processed', _hessian,  hessian_max,  change_hessian)
cv.CreateTrackbar('octive',   'Processed', _octive,   octive_max,   change_octive)
cv.CreateTrackbar('layer',    'Processed', _layer,    layer_max,    change_layer)

depth = pickle.load(open('depth.pickle', 'r'))
video = cv.LoadImageM('depth.jpg')
gray_base = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
gray_show = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(video, gray_base, cv.CV_RGB2GRAY)
#cv.ShowImage('Gray', gray_base)

while 1:
    if changed:
        changed = False

        cv.Canny(gray_base, gray_show, 50, 180)
        (keypoints, descriptors) = cv.ExtractSURF(gray_show, None, cv.CreateMemStorage(), (0, _hessian + 1, _octive + 1, _layer + 1))

        print 'len(keypoints):', len(keypoints)
        print 'keypoint[0]:', keypoints[0]
        c, cx, cy, cr = distance.closest(depth, [(int(x[0][0]), int(x[0][1]), x[2] / 2) for x in keypoints], 'point')
        print 'closest:', c, cx, cy, cr
        for ((y, x), laplacian, size, orient, hessian) in keypoints:

            #print "x=%d y=%d laplacian=%d size=%d orient=%f hessian=%f" % (x, y, laplacian, size, orient, hessian)
            radio = int(size*1.2/9.*2)
            #print "radioOld: ", int(radio)
            color = (255, 0, 0)
            #if radio < 3:
            #    radio = 2
            #    color = cv.Scalar(0, 255, 0)
            #print "radioNew: ", int(radio)
            cv.Circle(gray_show, (int(x), int(y)), radio, color)

        cv.ShowImage('Processed', gray_show)

        closest = cv.LoadImageM('depth.jpg')
        cv.Circle(closest, (cx, cy), int(cr + 1.2 / 9.), (0,255,0))
        cv.ShowImage('Closest', closest)

    key = cv.WaitKey(10)
    if key == 27:    # escape
        break
