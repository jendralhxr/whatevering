#!/usr/bin/python3
# python video2fps.py input.mp4 output.mp4 startframe endframe framestoskip
# 00000.MTS starts at 400
# 00001.MTS starts at 0

import numpy as np
import math
import cv2
import sys
import random
from datetime import datetime

THRESHOLD_VAL= 30
FRAME_STEP= 10

# margin in the actual image, to be cropped
startx= 880               
stopx= 4096
starty=0
stopy= 480

# image section to be processed, within cropped area
cropped_x_start= 0
cropped_x_stop= 3200 # shorter window makes life easier
cropped_y_start= 0
cropped_y_stop= 470

thickness_min_horizontal= 60 # maximum width of bondo
thickness_min_vertical= 10 # maximum width of bondo
block_width= 300 # minimum width of vehicle
update_interval= 200 # frames

cap = cv2.VideoCapture(sys.argv[1])
vsize = (int((stopx-startx)/4), int((stopy-starty)/4))

out = cv2.VideoWriter(sys.argv[2],cv2.VideoWriter_fourcc(*'mp4v'), 25.0, vsize)
framenum = int(sys.argv[3])
FRAME_STEP= int(sys.argv[5])

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print( "length of video: " + str(length) )


digit=8

while(1):
	ret, frame = cap.read()
	cropped = frame[starty:stopy, startx:stopx]
	
	#cv2.imshow('display',cropped)
	#cv2.imshow('display',image_display)
	#cv2.imshow('cue',image_cue)
	image_display_resized=cv2.resize(cropped, vsize, interpolation= cv2.INTER_AREA)
	#image_cue_resized = cv2.resize(image_cue, vsize, interpolation = cv2.INTER_AREA)
	#cv2.imshow('display',image_display_resized)
	#cv2.imshow('cue',image_cue_resized)
	   
	dateTimeObj = datetime.now()
	timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	
	#k = cv2.waitKey(1) & 0xFF
	#if k== ord("c"):
	#	print("saving: "+str(framenum).zfill(digit)+'.png')
	#	cv2.imwrite(str(framenum).zfill(digit)+'.png', cropped)
	#if k== 27: # esc
	#	break
	
	#out.write(cropped)
	#out2.write(image_cue)
	out.write(image_display_resized)
	#out2.write(image_cue_resized)
	
	print('time: ', timestampStr, "framenum: ", str(framenum));
	framenum += FRAME_STEP
	cap.set(cv2.CAP_PROP_POS_FRAMES, float(framenum))
	
	if framenum> int(sys.argv[4]):
		output.release()
		cap.release()
		break
	
cap.release()
out.release()
cv2.destroyAllWindows()
