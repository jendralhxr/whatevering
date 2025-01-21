#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:24:23 2025
@author: jendralhxr
"""
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('5394log.csv')
# Apply the moving average smoothing
window_size = 240
df['smoothed_count'] = df['count'].rolling(window=window_size, center=True).mean()

# Plot the original and smoothed data
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['count'], label='Original', alpha=0.5)
plt.plot(df['time'], df['smoothed_count'], label='Smoothed (Moving Average)', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Count')
plt.title('Count over Time with Moving Average Smoothing')
plt.xticks(range( int(min(df['time'])), int(max(df['time'])) + 1, 15))
plt.legend()
plt.grid(True)
plt.show()
