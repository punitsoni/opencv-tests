#!/usr/bin/python

import cv2
import numpy as np

print "-- OpenCV test --"
print "-----------------"

img = cv2.imread("res/lena.bmp")
print img.dtype
#print size(img)
r = img[:,:,2]
#print px

cv2.imshow("test", r)
print "press any key to continue"
cv2.waitKey(0)
