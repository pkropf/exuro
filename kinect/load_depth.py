#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv
import numpy
import pickle
import taber

depth  = pickle.load(open('depth.pickle', 'r'))
depthx = numpy.ma.masked_values(depth, 2047)
video  = cv.LoadImageM('depth.jpg')
gray   = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(video, gray, cv.CV_RGB2GRAY)

(keypoints, descriptors) = cv.ExtractSURF(gray, None, cv.CreateMemStorage(), (0, 8000, 4, 1))

x = [z[0][0] for z in keypoints]
y = [z[0][1] for z in keypoints]

print gray
print 'min(x):', min(x), 'max(x):', max(x)
print 'min(y):', min(y), 'max(y):', max(y)
