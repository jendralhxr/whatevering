#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 10:06:05 2024
@author: jendralhxr
"""

import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text  # Import the adjustText library

# Load data from the CSV file
csv_path = "knowledge_transfer_data.csv"  # Adjust the path if necessary
data = pd.read_csv(csv_path)

# Extract columns
countries = data["Country"].tolist()
objective = data["Objective"].tolist()
involvement = data["Involvement"].tolist()

# Create the scatter plot
plt.figure(figsize=(12, 7))
plt.scatter(objective, involvement, color='blue', alpha=0.7)

# Prepare the list of text objects (labels)
texts = []
for i, country in enumerate(countries):
    # Create a text object for each country
    text = plt.text(objective[i] + 0.1, involvement[i], country, fontsize=9)
    texts.append(text)

# Adjust text positions to avoid overlap
adjust_text(texts, arrowprops=dict(arrowstyle="->", color='red', lw=0.5))

# Set tick intervals
plt.xticks(range(-5, 6, 1))
plt.yticks(range(-5, 6, 1))

# Add horizontal and vertical axis lines
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')

# Add title and axis labels
plt.title("Knowledge Transfer in Computer Engineering", fontsize=14)
plt.xlabel("Cultural Collectivism (-), Monetary Profit (+) [Objective]", fontsize=12)
plt.ylabel("Community Empowerment (-), State Control (+) [Involvement]", fontsize=12)

# Add grid lines
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

# Display the plot
plt.tight_layout()
plt.show()
