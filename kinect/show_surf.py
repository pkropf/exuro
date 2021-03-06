#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2011 Peter Kropf. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import cv
import frame_convert
import copy
import pickle
import pygame
import Image
import time


_hessian    = 3000
hessian_max = 100000
_octive     = 4
octive_max  = 25
_layer      = 0
layer_max   = 25

def change_hessian(value):
    global _hessian
    _hessian = value

def change_octive(value):
    global _octive
    _octive = value

def change_layer(value):
    global _layer
    _layer = value


cv.NamedWindow('Depth')
cv.CreateTrackbar('hessian', 'Depth', _hessian, hessian_max, change_hessian)
cv.CreateTrackbar('octive',  'Depth', _octive,  octive_max,  change_octive)
cv.CreateTrackbar('layer',   'Depth', _layer,   layer_max,   change_layer)

depth = pickle.load(open('depth.pickle', 'r'))
video = cv.LoadImageM('depth.jpg')
gray = cv.CreateImage(cv.GetSize(video), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(video, gray, cv.CV_RGB2GRAY)

pygame.init()
ventana = pygame.display.set_mode((640, 480))
pygame.display.set_caption('depth')
screen = pygame.display.get_surface()

while 1:
    (keypoints, descriptors) = cv.ExtractSURF(gray, None, cv.CreateMemStorage(), (0, _hessian + 1, _octive + 1, _layer + 1))

    img_pil = Image.fromstring("RGB", cv.GetSize(video), video.tostring())
    pgimg = pygame.image.frombuffer(img_pil.tostring(), img_pil.size, img_pil.mode)

    print len(keypoints)
    for ((x, y), laplacian, size, dir, hessian) in keypoints:
        #print "x=%d y=%d laplacian=%d size=%d dir=%f hessian=%f" % (x, y, laplacian, size, dir, hessian)
        radio = size*1.2/9.*2
        #print "radioOld: ", int(radio)
        color = (255, 0, 0)
        if radio < 3:
            radio = 2
            color = (0, 255, 0)
        #print "radioNew: ", int(radio)
        pygame.draw.circle(pgimg, color, (x, y), radio, 2)

    screen.blit(pgimg, (0,0))
    pygame.display.flip()

    pil = Image.fromstring('RGB', (640, 480), pygame.image.tostring(pgimg, 'RGB'))
    cv_im = cv.CreateImageHeader(pil.size, cv.IPL_DEPTH_8U, 3)
    cv.SetData(cv_im, pil.tostring())

    cv.ShowImage('Depth', cv_im)

    key = cv.WaitKey(10)
    if key == 27:    # escape
        break
