#!/usr/bin/env python3
import numpy as np
import cv2
import sys
import math

print(sys.argv[1])
cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
frame = cap.read()
fgbg = cv2.createBackgroundSubtractorMOG2(400, 40, bool(0))

crop_x_start= 100
crop_x_stop= 450
crop_y_start= 8
crop_y_stop= 40

gate_right= 200
gate_left= 1200

thickness_min= 10 # maximum width of bondo
block_width= 60 # minimum width of vehicle
detector = cv2.SimpleBlobDetector()
    
framenum= 0
while(1):
    ret, frame = cap.read()
    framenum+=1
    #cropping
    image= frame[crop_y_start:crop_y_stop, crop_x_start:crop_x_stop]

    #fmask_gray = fgbg.apply(image)
    #fmask_rgb = cv2.cvtColor(fmask_gray, cv2.COLOR_GRAY2RGB);
    #result = cv2.bitwise_and(image, fmask_rgb)
     cv2.imshow('input',image)
    #cv2.imshow("Keypoints", im_with_keypoints)
    #cv2.imshow('output',result)
    k = cv2.waitKey(1)    
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
