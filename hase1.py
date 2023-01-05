import cv2
import sys
import numpy as np
    
traffic_start_x= 0;
traffic_start_y= 0;
traffic_end_x= 4096;
traffic_end_y= 232;

deck_start_x= 0;
deck_start_y= 232;
deck_end_x= 4096;
deck_end_y= 424;

girder_start_x= 0;
girder_start_y= 404;
girder_end_x= 4096;
girder_end_y= 636;

traffic_size = (traffic_end_x-traffic_start_x, traffic_end_y-traffic_start_y)
deck_size = (deck_end_x-deck_start_x, deck_end_y-deck_start_y)
girder_size = (girder_end_x-girder_start_x, girder_end_y-girder_start_y)

img = cv2.imread(sys.argv[1])
height, width, _ = img.shape

traffic_crop = img[traffic_start_y:traffic_end_y, traffic_start_x:traffic_end_x]
contours = np.array([ [0,232], [4096,232], [0, 152] ])
cv2.fillPoly(traffic_crop, pts =[contours], color=(255,255,255))
cv2.imwrite(sys.argv[2], traffic_crop)

deck_crop= img[deck_start_y:deck_end_y, deck_start_x:deck_end_x]
contours = np.array([ [0,170], [4096,180], [4096, 192], [0, 192] ])
cv2.fillPoly(deck_crop, pts =[contours], color=(0,0,0))
cv2.imwrite(sys.argv[3], deck_crop)

girder_crop= img[girder_start_y:girder_end_y, girder_start_x:girder_end_x]
contours = np.array([ [0,100], [0,232], [1370, 232], [1346, 100] ])
cv2.fillPoly(girder_crop, pts =[contours], color=(0,0,0))
contours = np.array([ [1580,232], [1696,232], [1696, 200], [1658, 200] ])
cv2.fillPoly(girder_crop, pts =[contours], color=(0,0,0))
contours = np.array([ [1760,150], [1760,232], [1854, 232], [1854, 150] ])
cv2.fillPoly(girder_crop, pts =[contours], color=(0,0,0))
contours = np.array([ [2926,66], [2926,232], [3082, 232], [3082, 66] ])
cv2.fillPoly(girder_crop, pts =[contours], color=(0,0,0))
contours = np.array([ [215,12], [215,112], [233, 112], [233, 12] ])
cv2.fillPoly(girder_crop, pts =[contours], color=(0,0,0))
contours = np.array([ [215,86], [215,112], [800, 112], [800, 86] ])
cv2.fillPoly(girder_crop, pts =[contours], color=(0,0,0))
cv2.imwrite(sys.argv[4], girder_crop)
    
scale=2
traffic_resized = cv2.resize(traffic_crop, (int(traffic_size[0]/scale), int(traffic_size[1]/scale)), interpolation = cv2.INTER_AREA)
deck_resized = +cv2.resize(deck_crop, (int(deck_size[0]/scale), int(deck_size[1]/scale)), interpolation = cv2.INTER_AREA)
girder_resized = cv2.resize(girder_crop, (int(girder_size[0]/scale), int(girder_size[1]/scale)), interpolation = cv2.INTER_AREA)

cv2.imshow('traffic',traffic_resized)
cv2.imshow('deck',deck_resized)
cv2.imshow('girder',girder_resized)

cv2.waitKey() & 0xFF
cv2.destroyAllWindows()