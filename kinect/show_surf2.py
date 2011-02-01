#!/usr/bin/env python

import cv
import frame_convert
import copy
import pickle
import time


_hessian    = 3000
hessian_max = 100000
_octive     = 4
octive_max  = 25
_layer      = 0
layer_max   = 25
changed     = True

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
cv.NamedWindow('Color')
cv.CreateTrackbar('hessian', 'Color', _hessian, hessian_max, change_hessian)
cv.CreateTrackbar('octive',  'Color', _octive,  octive_max,  change_octive)
cv.CreateTrackbar('layer',   'Color', _layer,   layer_max,   change_layer)

#depth = pickle.load(open('depth.pickle', 'r'))
video = cv.LoadImageM('depth.jpg')
gray_base = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
gray_show = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(video, gray_base, cv.CV_RGB2GRAY)

while 1:
    if changed:
        changed = False

        cv.Copy(gray_base, gray_show)
        (keypoints, descriptors) = cv.ExtractSURF(gray_base, None, cv.CreateMemStorage(), (0, _hessian + 1, _octive + 1, _layer + 1))

        print len(keypoints)
        for ((x, y), laplacian, size, dir, hessian) in keypoints:
            #print "x=%d y=%d laplacian=%d size=%d dir=%f hessian=%f" % (x, y, laplacian, size, dir, hessian)
            radio = size*1.2/9.*2
            #print "radioOld: ", int(radio)
            color = (255, 0, 0)
            if radio < 3:
                radio = 2
                color = cv.Scalar(0, 255, 0)
            #print "radioNew: ", int(radio)
            cv.Circle(gray_show, (x,y), radio, color)

        cv.ShowImage('Color', gray_show)

    key = cv.WaitKey(10)
    if key == 27:    # escape
        break
