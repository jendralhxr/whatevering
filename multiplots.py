#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:33:47 2025
@author: jendralhxr
"""

import numpy as np
import matplotlib.pyplot as plt

# Define the constant PHI (Golden Ratio)
PHI = (1 + np.sqrt(5)) / 2

# Define the function
def freqmin(x, coeff):
    return (1 - np.exp(-pow(PHI, -6) * x)) / pow(PHI, coeff)

# Define x values
x = np.linspace(0, 200, 400)

# Plot the function for COEFF from 4 to 10
plt.figure(figsize=(8, 6))
for coeff in range(2, 9):
    y = freqmin(x, coeff)
    plt.plot(x, y, label=f'COEFF={coeff}')

# Formatting the plot
plt.xlabel('hurf appearance')
plt.ylabel('substroke probability within hurfs')
#plt.title('Plot of freqmin(x) for COEFF from 4 to 10')
plt.legend()
plt.grid(True)
plt.show()
