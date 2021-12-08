#!/bin/env python3
import cv2
import numpy as np

frame = cv2.imread('image1.jpg', cv2.IMREAD_COLOR)

params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 1
params.maxThreshold = 255
params.filterByArea = True
params.minArea = 1
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False

detector = cv2.SimpleBlobDetector_create(params)

keypoints = detector.detect(frame)

cv2.drawKeypoints(frame, keypoints, frame, color=(0,0,255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow('grayscale image', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('image1_grayscale.jpg', frame)
