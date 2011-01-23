"""depth is a tuple of approximate depth in 
meters for a given value in the array returned 
from freenect.sync_get_depth()[0].

This is based on the work by Stéphane Magnenat 
in: https://groups.google.com/group/openkinect/browse_thread/thread/31351846fd33c78/e98a94ac605b9f21?lnk=gst&q=stephane&pli=1
"""

import math

depth = tuple([0.1236 * math.tan(x / 2842.5 + 1.1863) for x in range(2048)])
