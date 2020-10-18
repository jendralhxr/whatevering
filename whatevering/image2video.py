import cv2
import numpy as np
import glob
import sys
 
img_array = []
for filename in glob.glob(sys.argv[1]+'/*.png'):
    img = cv2.imread(filename)
    print(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    
out = cv2.VideoWriter(sys.argv[2],cv2.VideoWriter_fourcc(*'MP4V'), 60, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()