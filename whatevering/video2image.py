import cv2
import os
import sys

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
start= int(sys.argv[2])
stop = int(sys.argv[3])
n = start

startx= 1600
starty=600
stopx= 2400
stopy= 1640

#os.makedirs(dir_path, exist_ok=True)
#base_path = os.path.join(dir_path, basename)

digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
while n < stop:
    ret, frame = cap.read()
    cropped = frame[starty:stopy, startx:stopx]
    cv2.imwrite('{}/{}.png'.format(sys.argv[4], str(n).zfill(digit)), cropped)
    #cv2.imwrite('{}/{}.png'.format(sys.argv[4], str(n).zfill(digit)), frame)
    n += 1
    print(str(n).zfill(digit))
    