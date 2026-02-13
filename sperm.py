# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 12:05:35 2026

@author: rdx
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Load image and preprocess
img = cv2.imread('sperm.jpg', 0) # Load as grayscale
#blur = cv2.GaussianBlur(img, (5, 5), 0)

# # 2. Otsu's Thresholding
# ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
# plt.imshow(thresh, cmap='gray')

# ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_TRIANGLE)
# plt.imshow(thresh, cmap='gray')

# threshold_value = 155
# ret, thresh = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)
# plt.imshow(thresh, cmap='gray')


thresh_local = cv2.adaptiveThreshold(
    img, 255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY, 
    11, 2
)
plt.imshow(thresh_local, cmap='gray')

# TODO
## HAPUS noise di sini
## bikin erosion selektif

# 3. Edge Detection
edges = cv2.Canny(thresh, 100, 200)

# 4. Distance Transform 
# We invert the edges so that the distance is calculated FROM the edges
inv_edges = cv2.bitwise_not(edges)
dist_transform = cv2.distanceTransform(inv_edges, cv2.DIST_L2, 5)

# 5. Create a Color Output Image
output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

# asumsi lebar ekor
spacing_threshold = 4

# 6. Iterate through edge pixels and color them
# We look at the distance transform values *at* the edge locations 
# to see how much "empty space" is around them.
edge_coords = np.column_stack(np.where(edges > 0))

for y, x in edge_coords:
    # Check the neighborhood in the distance transform
    # We use a small offset to ignore the pixel itself
    val = dist_transform[y, x] 
    
    # Note: To truly find "neighboring" edges, we look at the distance 
    # value slightly adjacent to the edge pixel.
    surrounding_dist = np.mean(dist_transform[max(0, y-1):y+2, max(0, x-1):x+2])

    if surrounding_dist < spacing_threshold:
        output[y, x] = [0, 0, 255] # Red (ekor)
    else:
        output[y, x] = [0, 255, 0] # Green (kepala)

# TODO
# buat distribusi:
    # - panjang ekor
    # - ukuran (luas) kepala

