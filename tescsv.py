import numpy as np
import math
import cv2
import sys
import random
from datetime import datetime
import csv

cap = cv2.VideoCapture(sys.argv[1])

with open(sys.argv[2]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        for col in range(0,6):
            temp += float(row[col]);
        print(f'\t{temp}')
        #line_count += 1
    print(f'Processed {line_count} lines.')