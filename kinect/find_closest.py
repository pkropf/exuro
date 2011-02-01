#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import numpy as np


print 'loading scraped depth'
depth = pickle.load(open('depth.pickle', 'r'))
print type(depth)
print depth
print depth.min()
print depth.max()

for x in range(depth.shape[0]):
    hdepth, bdepth = np.histogram(depth[x], bins=10, range=(0.0, 2000.0))
    print x, hdepth
