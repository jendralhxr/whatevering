import cv2
import numpy as np
import glob
import sys

size = (1920,1024)
out = cv2.VideoWriter(sys.argv[2],cv2.VideoWriter_fourcc(*'MP4V'), 6, size)
 
for filename in glob.glob(sys.argv[1]+'/*.png'):
    img = cv2.imread(filename)
    imagename, ext= os.path.splitext(filename)
	freq= int(imagename)
    print(f"{freq} Hz: {filename}")
	cv.putText(ccv, f"{freq} Hz", (400, 200), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
    
out.release() 
