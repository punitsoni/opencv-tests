#!/usr/bin/env python

import cv2
import numpy as np

print "-- OpenCV test --"
print "-----------------"

img = cv2.imread("res/lena.bmp")
print img.ndim
print img.size
print img.shape
r = img[:,:,2]

c = np.zeros((1, 1, 3), np.uint8)
c[0, 0, :] = [135, 255, 255]
c1 = cv2.cvtColor(c, cv2.COLOR_HSV2BGR)

print tuple(c1[0, 0].tolist())

#cv2.imshow("test", r)
#print "press any key to continue"
#cv2.waitKey(0)