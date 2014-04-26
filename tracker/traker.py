#!/usr/bin/env python

import cv2
import numpy as np
from keycodes import *

def nothing(x):
  pass

class TargetTracker:

  _winTracker = "Tracker"
  _winMask = "Mask"
  _barHval = "Hue"
  _width = 320
  _height = 240
  _debugMode = False
  _shotNum = 0;

  def __init__(self):
    cv2.namedWindow(self._winTracker)
    cv2.moveWindow(self._winTracker, 10, 10)
    cv2.createTrackbar(self._barHval, self._winTracker, 100, 180, nothing)
    cv2.createTrackbar("H max", self._winTracker, 120, 180, nothing)

    self._capture = cv2.VideoCapture(-1)
    self._capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self._width)
    self._capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self._height)

  def initDebugMode(self):
    cv2.namedWindow(self._winMask)
    cv2.moveWindow(self._winMask, 10, self._height+50)
  def deinitDebugMode(self):
    cv2.destroyWindow(self._winMask)

  def run(self):
    print 'Showing camera feed. Click window or press any key to stop.'
    success, frame = self._capture.read()
    while success:
      frame = np.fliplr(frame).copy()
      self.processImage(frame)
      cv2.imshow(self._winTracker, frame)
      #cv2.imshow(self._winMask, mask)
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
        cv2.imwrite("screenshot" + str(self._shotNum) + ".png", frame)
      # next frame
      success, frame = self._capture.read()

  def cleanup(self):
    cv2.destroyAllWindows()

  def processImage(self, frame):
    blur = cv2.GaussianBlur(frame, (7,7), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    Hmin = cv2.getTrackbarPos(self._barHval, self._winTracker)
    Hmax = cv2.getTrackbarPos("H max", self._winTracker)

    blue_min = np.array([Hmin-10, 50, 20], np.uint8)
    blue_max = np.array([Hmin+10, 255, 255], np.uint8)

    mask = cv2.inRange(hsv, blue_min, blue_max)
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    if self._debugMode == True:
      self.initDebugMode()
      imshow(self._winMask, mask)
    else:
      self.deinitDebugMode()

    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
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
      cv2.drawContours(frame, [largestCnt], 0, (0,255,0), 1)

    c = np.zeros((1, 1, 3), np.uint8)
    c[0, 0, :] = [Hmin, 255, 255]
    c = cv2.cvtColor(c, cv2.COLOR_HSV2BGR)

    cv2.rectangle(frame, (0, 0), (20, 20), tuple(c[0, 0].tolist()), -1)

    '''rect = cv2.minAreaRect(largestCnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box), 3
    frame = cv2.drawContours(frame,[box],0,(0,0,255),2)'''
# end of TargetTracker

# main
if __name__ == "__main__":
  tracker = TargetTracker()
  tracker.run()
  tracker.cleanup()
  print "finished."

