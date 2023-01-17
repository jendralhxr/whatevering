#!/usr/bin/python3
# python -u mergeside.py left_image right_image offset_column output_image
# use to make 'empty' background image

import numpy as np
import math
import cv2 as cv
import sys
import csv

img_left= cv.imread(sys.argv[1])
img_right= cv.imread(sys.argv[2])
offset= int(sys.argv[3])
img_output = sys.argv[4]

height= int(img_left.shape[0])
width= int(img_left.shape[1])
print("{}x{}".format(width, height))

#left_part= img_left[0:height-1, 0:offset]
img_right[0:height-1, 0:offset]= img_left[0:height-1, 0:offset]
#cv.imshow('display',img_right)
cv.imwrite(img_output, img_right)

# while 1:
    # k = cv.waitKey(1) & 0xFF
    # if k== 27: # esc
        # break
