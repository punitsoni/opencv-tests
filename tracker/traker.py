#!/usr/bin/env python

import cv2
import numpy as np
from keycodes import *

def nothing(x):
  pass

class TargetTracker:

  _winTracker = "Tracker"
  _winMask = "Mask"
  _width = 320
  _height = 240

  def __init__(self):
    cv2.namedWindow(self._winTracker)
    #cv2.namedWindow(self._winMask)
    cv2.moveWindow(self._winTracker, 10, 10)
    #cv2.moveWindow(self._winMask, 10, self._height+50)
    cv2.createTrackbar("H min", self._winTracker, 100, 255, nothing)
    cv2.createTrackbar("H max", self._winTracker, 120, 255, nothing)

    self._capture = cv2.VideoCapture(-1)
    self._capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self._width)
    self._capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self._height)

  def run(self):
    print 'Showing camera feed. Click window or press any key to stop.'
    success, frame = self._capture.read()
    while success:
      frame = np.fliplr(frame).copy()
      self.processImage(frame)
      cv2.imshow(self._winTracker, frame)
      #cv2.imshow(self._winMask, mask)
      success, frame = self._capture.read()
      key = cv2.waitKey(10)

      if key == KEY_ESC:
        break;
      elif key == KEY_ALPHA('p'):
        while True:
          key1 = cv2.waitKey(10)
          if key1 == KEY_ALPHA('p'):
            break;
      elif key == KEY_SPC:
        print "Take Screenshot"

  def cleanup(self):
    cv2.destroyAllWindows()

  def processImage(self, frame):
    blur = cv2.GaussianBlur(frame, (7,7), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    Hmin = cv2.getTrackbarPos("H min", self._winTracker)
    Hmax = cv2.getTrackbarPos("H max", self._winTracker)

    blue_min = np.array([Hmin, 50, 20], np.uint8)
    blue_max = np.array([Hmax, 255, 255], np.uint8)

    mask = cv2.inRange(hsv, blue_min, blue_max)
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    #print len(contours)
    largestCnt = None
    maxArea = 0
    for cnt in contours:
      area = cv2.contourArea(cnt)
      if area > maxArea:
        maxArea = area
        largestCnt = cnt

    print maxArea
    if maxArea > 100.0:
      M = cv2.moments(largestCnt)
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])
      print "center:", cx, cy
      cv2.circle(frame, (cx, cy), 3, (0, 0, 255))
      frame = cv2.drawContours(frame, [largestCnt], 0, (0,255,0), 1)

    '''rect = cv2.minAreaRect(largestCnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    frame = cv2.drawContours(frame,[box],0,(0,0,255),2)'''
    
  def getThreshImage(self, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    ORANGE_MIN = np.array([8, 200, 60],np.uint8)
    ORANGE_MAX = np.array([12, 255, 255],np.uint8)

    result = cv2.inRange(hsv, ORANGE_MIN, ORANGE_MAX)

    #kernel = np.ones((3,3),np.uint8)

    kernel = np.array([(0, 1, 0), (1, 1, 1), (0, 1, 0)], np.uint8)

    #result = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=6)

    #result = cv2.erode(result, kernel, iterations=1)
    result = cv2.dilate(result, kernel, iterations=3)
    return result

# main
if __name__ == "__main__":
  tracker = TargetTracker()
  tracker.run()
  tracker.cleanup()
  print "finished."

