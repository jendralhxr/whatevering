#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 09:33:36 2025

@author: rdx
"""

import mss
import mss.tools

with mss.mss() as sct:
    # Full screen
    sct.shot(output="full_screenshot.png")

    # Partial screen
    monitor = {"top": 100, "left": 100, "width": 640, "height": 480}
    img = sct.grab(monitor)
    mss.tools.to_png(img.rgb, img.size, output="partial_screenshot.png")
