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
import numpy
import pickle
import taber

def closest(depth, areas, check='mean'):
    close = 2049
    location = None

    depthm = numpy.ma.masked_values(depth, 2047)

    for x, y, radius in areas:
        if check == 'mean':

            if x - radius < 0:
                x = radius

            if y - radius < 0:
                y = radius

            x1 = x - radius
            x2 = x1 + (radius * 2)
            y1 = y - radius
            y2 = y1 + (radius * 2)

            mean = depthm[x1:x2, y1:y2].mean()
            #print x, y, radius, mean
            if mean < close:
                close = mean
                location = (x, y, radius)

        elif check == 'point':
            print x, y, radius
            print depthm.shape
            if depthm[x, y] < close:
                close = depthm[x, y]
                location = (x, y, radius)

    return close, location[0], location[1], location[2]


if __name__ == '__main__':
    depth = pickle.load(open('depth.pickle', 'r'))

    places = [(464, 45, 9),
              (42, 116, 7),
              (49, 134, 8),
              (502, 146, 8),
              (102, 150, 4),
              (496, 150, 7),
              (95, 154, 9),
              (83, 160, 6),
              (14, 167, 6),
              (15, 175, 8),
              (21, 186, 7),
              (74, 187, 7),
              (21, 192, 7),
              (47, 192, 6),
              (39, 197, 6),
              (94, 199, 6),
              (117, 200, 7),
              (35, 201, 8),
              (16, 201, 8),
              (235, 204, 7),
              (243, 205, 7),
              (56, 210, 7),
              (249, 209, 7),
              (243, 214, 8),
              (52, 216, 8),
              (57, 220, 7),
              (59, 221, 7),
              (253, 222, 7),
              (50, 224, 6),
              (61, 225, 7),
              (367, 225, 8),
              (26, 230, 8),
              (56, 232, 8),
              (250, 238, 8),
              (353, 239, 7),
              (34, 240, 6),
              (59, 242, 7),
              (255, 244, 8),
              (42, 247, 6),
              (250, 250, 7),
              (353, 251, 7),
              (341, 258, 7),
              (38, 260, 7),
              (82, 262, 7),
              (364, 262, 8),
              (34, 266, 9),
              (56, 268, 7),
              (348, 276, 7),
              (30, 280, 7),
              (36, 282, 6),
              (247, 283, 7),
              (89, 284, 8),
              (41, 287, 7),
              (291, 287, 7),
              (63, 288, 7),
              (325, 292, 8),
              (113, 293, 8),
              (302, 296, 7),
              (373, 296, 7),
              (61, 296, 7),
              (29, 299, 8),
              (330, 299, 8),
              (363, 301, 8),
              (289, 305, 6),
              (298, 306, 9),
              (505, 306, 8),
              (31, 306, 8),
              (263, 307, 7),
              (99, 310, 6),
              (342, 309, 8),
              (498, 310, 7),
              (522, 309, 8),
              (46, 311, 7),
              (38, 311, 7),
              (518, 323, 7),
              (35, 335, 8),
              (13, 337, 8),
              (284, 338, 7),
              (33, 342, 7),
              (205, 361, 7),
              (215, 366, 7),
              (229, 379, 8),
              (235, 412, 7),
              (180, 432, 8),
              (34, 140, 14),
              (98, 142, 15),
              (88, 146, 14),
              (112, 147, 14),
              (76, 151, 14),
              (39, 152, 17),
              (96, 159, 16),
              (112, 160, 13),
              (48, 164, 15),
              (87, 170, 13),
              (35, 185, 17),
              (272, 190, 15),
              (116, 195, 15),
              (244, 202, 16),
              (230, 208, 15),
              (120, 219, 15),
              (39, 219, 16),
              (54, 220, 15),
              (91, 225, 16),
              (47, 236, 16),
              (358, 245, 15),
              (273, 248, 15),
              (342, 248, 16),
              (358, 247, 15),
              (532, 253, 13),
              (61, 255, 14),
              (139, 256, 17),
              (80, 267, 14),
              (328, 280, 15),
              (341, 288, 16),
              (89, 290, 16),
              (370, 291, 17),
              (319, 291, 15),
              (387, 292, 14),
              (399, 291, 14),
              (500, 297, 15),
              (310, 307, 15),
              (29, 310, 15),
              (260, 310, 15),
              (528, 315, 14),
              (282, 346, 15),
              (31, 387, 12),
              (244, 403, 15),
              (260, 401, 13),
              (188, 406, 14),
              (185, 418, 15),
              (199, 427, 15),
              (198, 443, 15),
              (117, 457, 18),
              (189, 455, 13),
              (90, 134, 29),
              (397, 182, 34),
              (394, 215, 29),
              (77, 226, 33),
              (317, 265, 30),
              (359, 267, 28),
              (312, 297, 33),
              (110, 299, 27),
              (335, 313, 30),
              (512, 312, 36),
              (313, 330, 29),
              (97, 335, 29),
              (105, 255, 57),
              (343, 337, 59),
              (361, 339, 60),
              (454, 235, 117),
              ]

    places2 = [(10, 10, 3), (100, 100, 10), (200, 200, 20)]
    print closest(depth, places)
