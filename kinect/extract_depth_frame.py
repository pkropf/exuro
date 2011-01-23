#!/usr/bin/env python
import freenect
import cv
import frame_convert
import copy
import pickle

cv.NamedWindow('Depth')
cv.NamedWindow('Video')
print('Press ESC in window to stop')

depth = None
scrape = True

def get_depth():
    global depth
    global scrape

    if scrape:
        print 'scraping a new depth'
        depth = freenect.sync_get_depth()[0]
        #print depth
        pickle.dump(depth, open('depth.pickle', 'w'))
        scrape = False

    return frame_convert.pretty_depth_cv(copy.deepcopy(depth))


def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])


while 1:
    cv.ShowImage('Depth', get_depth())
    cv.ShowImage('Video', get_video())

    key = cv.WaitKey(10)
    if key == 27:    # escape
        break

    elif key == 115: # lower case s
        scrape = True

