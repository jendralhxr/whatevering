# for i in `seq 1 100`; do 
# python -u vidphasecorrelate.py input.avi output.mp4 output.csv frame_start frame_end
# python -u vidphasecorrelate.py $i.avi output${i}.mp4 log${i}.csv

# done

import numpy as np
import math
import cv2 as cv
import sys
import csv

cap = cv.VideoCapture(sys.argv[1])
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
fps = cap.get(cv.CAP_PROP_FPS);
frame_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print("input video is: {}x{} @{} {}".format(width, height, fps,  frame_length) )    

vid_output = cv.VideoWriter(sys.argv[2],cv.VideoWriter_fourcc(*'mp4v'), 500, (width, height))

FS= 500
N=256

ROI_NUM= 7

xmin = np.zeros(ROI_NUM, dtype=np.uint16)
xmax = np.zeros(ROI_NUM, dtype=np.uint16)
ymin = np.zeros(ROI_NUM, dtype=np.uint16)
ymax = np.zeros(ROI_NUM, dtype=np.uint16)
xmid = np.zeros(ROI_NUM, dtype=np.uint16)
ymid = np.zeros(ROI_NUM, dtype=np.uint16)
xmid = np.zeros(ROI_NUM, dtype=np.uint16)
ymid = np.zeros(ROI_NUM, dtype=np.uint16)
# finger:
xmin[6],xmax[6],ymin[6],ymax[6]= 266,371,400,512
#wrist:
xmin[5],xmax[5],ymin[5],ymax[5]= 265,365,261,375
#arm1:
xmin[4],xmax[4],ymin[4],ymax[4]= 383,507,142,255
#arm2:
xmin[3],xmax[3],ymin[3],ymax[3]= 784,894,275,380
#base1:
xmin[2],xmax[2],ymin[2],ymax[2]= 776,884,518,626
#base:
xmin[1],xmax[1],ymin[1],ymax[1]= 756,898,774,878
#plate
xmin[0],xmax[0],ymin[0],ymax[0]= 877,901,943,965

dx=np.zeros(ROI_NUM,dtype='float64');
dy=np.zeros(ROI_NUM,dtype='float64');
              
csvlog = open(sys.argv[3], 'w', newline='')
writer = csv.writer(csvlog)
header= ['framenum','0x','0y','1x','1y','2x','2y','3x','3y','4x','4y','5x','5y','6x','6y']
writer.writerow(header);

startframe= int(sys.argv[4])
framenum= startframe;
cap.set(cv.CAP_PROP_POS_FRAMES, float(startframe))
lastframe= int(sys.argv[5])


ARROW_AMP= 10;

while (framenum<frame_length-1) and (framenum<lastframe):
    # read frame from video
    ret, current_col = cap.read()
    current_gray = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)
    for i in range(ROI_NUM):
        cv.rectangle(current_col, (xmin[i],ymin[i]), (xmax[i], ymax[i]), (0,255,0), 2)
        xmid[i]= int( (xmin[i]+xmax[i])/2 )
        ymid[i]= int( (ymin[i]+ymax[i])/2 )
        
    if (framenum==startframe):
        start_gray= current_gray
        
    # calculate phase 
    for i in range(ROI_NUM):
        ref= start_gray[ymin[i]:ymax[i], xmin[i]:xmax[i]]
        roi= current_gray[ymin[i]:ymax[i], xmin[i]:xmax[i]]
        d, etc = cv.phaseCorrelate(roi.astype(np.float64), ref.astype(np.float64))
        dx[i], dy[i] =d
                    
    # the output
    numlist= [framenum];
    for i in range(ROI_NUM):
        numlist.append("{},{}".format(dx[i], dy[i]))
        # x=float(poc[0][0])
        # y=float(poc[0][1])
        # z=float(poc[1])
        cv.arrowedLine(current_col, (xmid[i], ymid[i]), (int(xmid[i]+dx[i]*ARROW_AMP), int(ymid[i]+dy[i]*ARROW_AMP)), (0, 0, 255), 4);
    writer.writerow(numlist);
    
    print(framenum)
    framenum += 1
    
    vid_output.write(current_col);
    # cv.imshow('cue',current_col)
    # k = cv.waitKey(1) & 0xFF
    # if k== 27: # esc
       # break

cap.release
vid_output.release
