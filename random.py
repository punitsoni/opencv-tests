#!/usr/bin/env python

import cv2
import os
import numpy

#image = cv2.imread("test.png", cv2.CV_LOAD_IMAGE_GRAYSCALE)
#cv2.imwrite("test-out.png", image)

# Make an array of 120,000 random bytes.
randomByteArray = bytearray(os.urandom(120000))
flatNumpyArray = numpy.array(randomByteArray)

# Convert the array to make a 400x300 grayscale image.
grayImage = flatNumpyArray.reshape(300, 400)
cv2.imwrite('RandomGray.png', grayImage)

# Convert the array to make a 400x100 color image.
bgrImage = flatNumpyArray.reshape(100, 400, 3)
cv2.imwrite('RandomColor.png', bgrImage)