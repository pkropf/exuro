#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv
import numpy
import pickle
import taber

depth = pickle.load(open('depth.pickle', 'r'))
