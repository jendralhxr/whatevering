#!/usr/bin/env python3
import numpy as np
import cv2
import sys
import math
import random

#  minyak.py filename frameoffset threshold starty stopy

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
detection_line= int(sys.argv[3])
y_start= int(sys.argv[5])
y_stop= int(sys.argv[6])
y_span= y_stop -y_start;
y_mid= int (y_start+ y_span/2);
print("y: {} {} {} {}".format(y_start, y_stop, y_mid, y_span));
    
frame_width= int (cap.get(cv2.CAP_PROP_FRAME_WIDTH));
frame_height= int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT));
threshold_bin= int(sys.argv[4]);
radius= 16;
step= 10;
    
framenum= 0
ret, frame = cap.read()
prev= frame;

edge_left= [0] * y_span;
edge_right= [0] * y_span;

while(1):
    ret, frame = cap.read()
    framenum+=1
        
    crop= frame[y_start:y_stop, 0:frame_width];
    ret,cue = cv2.threshold(crop, threshold_bin, 255, cv2.THRESH_BINARY);
	
    # assign existing ID, either from current or neighboring pixel in previous cue
    for j in range(0, y_span):
        for i in range(detection_line+1, frame_width):
            pix_jk= 0;
            if (cue.item(j,i,1) == 255):
                # ID from previous frame
                if (prev.item(j,i,1) != 255) and (prev.item(j,i,1) != 0):
                #    cue.itemset((j,i,1), prev.item(j,i,1));
                    pix_jk= 1;
                # ID from neighboring pixel
                #elif (cue.item(j,i-1,0) != 255) and (cue.item(j,i-1,0) != 0):
                #    cue.itemset((j,i,0), cue.item(j,i-1,0));
                #    pix_jk= 1;
                # blank it out if no ID is assigned    
                #if pix_jk==0:
                else:
                    pix_jk=0;
                    #cue.itemset((j,i,1), 0);
                
                
    # find blob edges
    for j in range(0, y_span):
        # find left edge
        for i in range(detection_line, detection_line-2*radius, -1):
            if (cue.item(j,i,0) == 0):
                edge_left[j]= i;
                break;
        # find right edge
        for i in range(detection_line, detection_line+2*radius):
            if (cue.item(j,i,0) == 0):
                edge_right[j]= i;
                break; 
    
    # fill in the blob if convex meniscus
    blob_id= random.randint(30, 230)
    #blob_id= 50;
    belt_cen= edge_right[y_mid-y_start] - edge_left[y_mid-y_start];
    belt_lat= edge_right[y_mid-y_start-step] - edge_left[y_mid-y_start-step];
    #print("{} {} {} {}".format(edge_right[y_mid-y_start], edge_left[y_mid-y_start], edge_right[y_mid-y_start-10], edge_left[y_mid-y_start-10] ));
    if (belt_cen > radius) and (belt_cen > belt_lat):
        print("{} {}".format(belt_cen, belt_lat));
        for j in range(0, y_span):
            for i in range(edge_left[j], edge_right[j]):
                if (cue.item(j,i,1) == 255):
                    cue.itemset((j,i,1), blob_id);
    
    prev= cue;
    
    # display
    for j in range(0, y_span):
        frame.itemset((j,detection_line,1) , 255) # green
        cue.itemset((j,detection_line,1) , 255) # green
    cv2.imshow('input',frame);
    cv2.imshow('output',cue);
    
    k = cv2.waitKey(20)    
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
