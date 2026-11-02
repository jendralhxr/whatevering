#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:51:01 2026

@author: rdx
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define bands and features
bands = [
    "Infrasound (0-20Hz)",
    "SubBass (20-50Hz)",
    "PowerLine (50-120Hz)",
    "CoreVocal (120-1000Hz)",
    "Telephony (1000-3500Hz)",
    "Audiophile (3500-20000Hz)",
    "Ultrasonic (20000Hz+)"
]

features = ["PeakWander", "PSNR", "TDR", "CrestFactor", "HPR"]

# Create data matrix for Cohen's d (|d|)
data = np.array([
    [0.000, 0.159, 0.269, 1.193, 0.000],  # Infrasound
    [1.856, 0.598, 0.839, 0.046, 0.000],  # SubBass
    [1.153, 0.787, 0.855, 1.012, 0.000],  # PowerLine
    [0.907, 1.303, 1.045, 0.184, 0.518],  # CoreVocal
    [0.550, 1.502, 1.343, 0.197, 0.000],  # Telephony
    [0.603, 1.513, 1.492, 0.312, 0.000],  # Audiophile
    [0.021, 0.811, 0.664, 0.917, 0.000]   # Ultrasonic
])

df = pd.DataFrame(data, index=bands, columns=features)

# Plotting 2D Heatmap
plt.figure(figsize=(10, 6))
sns.set_theme(style="white")

ax = sns.heatmap(
    df, 
    annot=True, 
    fmt=".3f", 
    cmap="YlGnBu", 
    cbar_kws={'label': "Cohen (|d|) Separation"},
    linewidths=0.5,
    linecolor='gray'
)

#plt.title("Separation Strength (Cohen's d) by Frequency Band & Audio Feature Metric", fontsize=12, pad=15)
plt.xlabel("Audio Feature Metric", fontsize=11, labelpad=10)
plt.ylabel("Frequency Band", fontsize=11, labelpad=10)
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.tight_layout()

plt.savefig("cohens_d_heatmap.png", dpi=300)
plt.show()