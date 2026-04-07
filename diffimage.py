#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 08:44:45 2026

@author: rdx
"""

import cv2
import sys
import numpy as np

def calculate_image_diff(img1_path, img2_path):
    # 1. Load the images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("Error: Could not load one or both images. Check your paths.")
        return

    # 2. Get dimensions of the first image (height, width)
    height, width = img1.shape[:2]

    # 3. Scale the second image to match the first
    # Interpolation choice: INTER_AREA is usually best for shrinking, 
    # INTER_CUBIC/LINEAR for enlarging.
    img2_scaled = cv2.resize(img2, (width, height), interpolation=cv2.INTER_AREA)

    # 4. Calculate the absolute difference
    # This ensures (Pixel A - Pixel B) doesn't result in negative numbers
    diff = cv2.absdiff(img1, img2_scaled)

    # 5. Save the result
    cv2.imwrite('diff.png', diff)
    print(f"Success: Difference saved to diff.png ({width}x{height})")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <image1> <image2>")
    else:
        calculate_image_diff(sys.argv[1], sys.argv[2])