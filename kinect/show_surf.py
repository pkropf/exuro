#!/usr/bin/env python

import cv
import frame_convert
import copy
import pickle


depth = pickle.load(open('depth.pickle', 'r'))
video = cv.LoadImageM('depth.jpg')
gray = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(video, gray, cv.CV_RGB2GRAY)

(keypoints, descriptors) = cv.ExtractSURF(gray, None, cv.CreateMemStorage(), (0, 3000, 3, 1))

#print keypoints
#print descriptors

for ((x, y), laplacian, size, dir, hessian) in keypoints:
    print "x=%d y=%d laplacian=%d size=%d dir=%f hessian=%f" % (x, y, laplacian, size, dir, hessian)

