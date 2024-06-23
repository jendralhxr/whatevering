#!/usr/bin/python

import cv2
import os
import sys

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
ret, frame = cap.read()
cv2.imwrite(sys.argv[3], frame)
