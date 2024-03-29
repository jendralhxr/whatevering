#!/usr/bin/python3
# python multicrop.py input.mp4 output1.mp4 output2.mp4 output3.mp4 lastframe

import numpy as np
import math
import cv2
import sys
import random
from datetime import datetime

# margin in the actual image, to be cropped
traffic_start_x= 0;
traffic_start_y= 0;
traffic_end_x= 4096;
traffic_end_y= 232;

deck_start_x= 0;
deck_start_y= 246;
deck_end_x= 4096;
deck_end_y= 334;

girder_start_x= 0;
girder_start_y= 428;
girder_end_x= 4096;
girder_end_y= 500;

FRAME_STEP= 1;

traffic_size = (traffic_end_x-traffic_start_x, traffic_end_y-traffic_start_y)
deck_size = (deck_end_x-deck_start_x, deck_end_y-deck_start_y)
girder_size = (girder_end_x-girder_start_x, girder_end_y-girder_start_y)

cap = cv2.VideoCapture(sys.argv[1])
if not cap.isOpened():
    sys.exit()
else:
    # Video Parameters
    IM_SIZE_Y = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));
    IM_SIZE_X = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT));
    CameraFrameRate = 100;
    length = cap.get(cv2.CAP_PROP_FRAME_COUNT);
    print("video is {}x{} px @{} fps for {} frames".format(IM_SIZE_Y, IM_SIZE_X, CameraFrameRate, length))
    out_traffic = cv2.VideoWriter(sys.argv[2],cv2.VideoWriter_fourcc(*'mp4v'), 100.0, traffic_size)
    out_deck = cv2.VideoWriter(sys.argv[3],cv2.VideoWriter_fourcc(*'mp4v'), 100.0, deck_size)
    out_girder = cv2.VideoWriter(sys.argv[4],cv2.VideoWriter_fourcc(*'mp4v'), 100.0, girder_size)

framenum = int(sys.argv[5])

digit=6

while(1):
	ret, frame = cap.read()
	
	traffic_crop = frame[traffic_start_y:traffic_end_y, traffic_start_x:traffic_end_x]
	deck_crop= frame[deck_start_y:deck_end_y, deck_start_x:deck_end_x]
	girder_crop= frame[girder_start_y:girder_end_y, girder_start_x:girder_end_x]
	
	#k = cv2.waitKey(1) & 0xFF
	#if k== ord("c"):
	#	print("saving: "+str(framenum).zfill(digit)+'.png')
	#	cv2.imwrite(str(framenum).zfill(digit)+'.png', cropped)
	#if k== 27: # esc
	#	break
	
	out_traffic.write(traffic_crop)
	out_deck.write(deck_crop)
	out_girder.write(girder_crop)
	
	framenum += FRAME_STEP
	print( "frame: ",framenum,"/",length)
	cap.set(cv2.CAP_PROP_POS_FRAMES, float(framenum))
	
	#if framenum> length:
	if framenum> int(sys.argv[6]):
		out_traffic.release()
		out_deck.release()
		out_girder.release()
		cap.release()
		break
	
cap.release()
out_traffic.release()
out_deck.release()
out_girder.release()
cv2.destroyAllWindows()
