#!/usr/bin/python

import cv2
import os
import sys
import subprocess

#cap = cv2.VideoCapture(sys.argv[1])
videoname, ext= os.path.splitext(sys.argv[1])
framenumber= int(sys.argv[2])
outputfile= videoname+'-'+sys.argv[2]+'.png'

ffmpeg_command = [
    'ffmpeg',
    '-i', sys.argv[1],
    '-vf', f'select=eq(n\,{framenumber})',
    '-vsync', 'vfr',
    outputfile
]
try:
    subprocess.run(ffmpeg_command, check=True)
    print(f"Successfully snapped frame {framenumber} to {outputfile}")
except subprocess.CalledProcessError as e:
    print(f"Error snapping frame {framenumber}: {e}")



#cap.set(cv2.CAP_PROP_POS_FRAMES, framenumber/10800)
#ret, frame = cap.read()
#if ret:
    # Display or process the frame
    #cv2.imshow('Frame', frame)
    #cv2.waitKey(0)  # Wait for any key press
    #cv2.imwrite(, frame)

