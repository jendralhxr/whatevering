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
crop= frame[y_start:y_stop, 0:frame_width];
prev= crop;
cue=  crop;

edge_left= [0] * y_span;
edge_right= [0] * y_span;
midline= int (y_span/2);

while(1):
    ret, frame = cap.read()
    framenum+=1
        
    crop= frame[y_start:y_stop, 0:frame_width];
    ret,cue = cv2.threshold(crop, threshold_bin, 255, cv2.THRESH_BINARY);
	
    print("---------------");
    blob_start= detection_line;
    blob_end= detection_line;
    for x in range (0, frame_width-1):
        # measure blob width
        if (cue.item(midline, x, 1) == 255) and (blob_start == blob_end):
            blob_start= x;
        if (cue.item(midline, x, 1) == 0) and (blob_end != blob_start):
            blob_end= x;
            new_id= random.randint(30, 230);
            old_id= prev.item( midline, int((blob_end+blob_start)/2)+2, 1);
            # apply old ID if possible
            if (old_id != 255) and (old_id != 0):
                print("{} {} {}". format(blob_start, blob_end, old_id));
                for blob_x in range (blob_start, blob_end):
                    cue.itemset((midline, blob_x, 1), old_id);
                # else, assign new ID
            elif (detection_line > blob_start) and (detection_line < blob_end):  
                #print("{} {} {}". format(blob_start, blob_end, new_id));
                for blob_x in range (blob_start, blob_end):
                    cue.itemset((midline, blob_x, 1), new_id);
            blob_start= blob_end;    

    # apply the watersehd
    # (optional) detect blob shape: concentricity, particle, etc
    for x in range(detection_line, frame_width-2):
        # assign ID from neighboring pixel
        # upward
        for y in range(midline, 0, -1):
            if (cue.item( y, x, 1)== 255) and (cue.item( y+1, x, 1)!= 255):
                cue.itemset(y, x, 1, cue.item( y+1, x, 1));
            elif (cue.item( y, x, 1)== 255) and (cue.item( y+1, x+1, 1)!= 255):
                cue.itemset(y, x, 1, cue.item( y+1, x+1, 1));
            elif (cue.item( y, x, 1)== 255) and (cue.item( y+1, x-1, 1)!= 255):
                cue.itemset(y, x, 1, cue.item( y+1, x-1, 1));
            if (cue.item( y, x, 1)== 0):
                break;
        # downward
        for y in range(midline, y_span, 1):
            if (cue.item( y, x, 1)== 255) and (cue.item( y-1, x, 1)!= 255):
                cue.itemset(y, x, 1, cue.item( y-1, x, 1));
            elif (cue.item( y, x, 1)== 255) and (cue.item( y-1, x+1, 1)!= 255):
                cue.itemset(y, x, 1, cue.item( y-1, x+1, 1));
            elif (cue.item( y, x, 1)== 255) and (cue.item( y-1, x-1, 1)!= 255):
                cue.itemset(y, x, 1, cue.item( y-1, x-1, 1));
            if (cue.item( y, x, 1)== 0):
                break;
        
    
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
