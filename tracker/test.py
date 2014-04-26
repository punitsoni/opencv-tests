import cv2
import numpy as np

def processImage(frame):
  blur = cv2.GaussianBlur(frame, (7,7), 0)
  hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

  blue_min = np.array([100, 50, 20], np.uint8)
  blue_max = np.array([110, 255, 255], np.uint8)

  mask = cv2.inRange(hsv, blue_min, blue_max)
  kernel = np.ones((3,3),np.uint8)
  mask = cv2.dilate(mask, kernel, iterations=1)

  contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                                         cv2.CHAIN_APPROX_SIMPLE)
  print len(contours)
  largestCnt = None
  maxArea = 0
  for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > maxArea:
      maxArea = area
      largestCnt = cnt

  print maxArea
  if maxArea > 0:
    M = cv2.moments(largestCnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print "center:", cx, cy
  '''rect = cv2.minAreaRect(largestCnt)
  box = cv2.boxPoints(rect)
  box = np.int0(box)
  frame = cv2.drawContours(frame,[box],0,(0,0,255),2)'''
  frame = cv2.drawContours(frame, [largestCnt], 0, (0,255,0), 1)

frame = cv2.imread("blue.png")
processImage(frame)
cv2.imshow("img", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()