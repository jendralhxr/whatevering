import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv('traffic.csv')  # replace with your actual filename
column_title= 'total'


# Extract the 'ongkos' data series
data = df[column_title].dropna().values  # drop NaNs if any

# Calculate mean and set std deviation to 20% of the mean
mean = np.mean(data)
std = 0.20 * mean

# Monte Carlo simulation
n_simulations = int(1e6)
simulations = np.random.normal(loc=mean, scale=std, size=(n_simulations, len(data)))

# Analyze: mean per simulation
simulated_means = np.mean(simulations, axis=1)

# Plot histogram of simulated means
plt.hist(simulated_means, bins=30, color='orange', edgecolor='black')
#plt.axvline(mean, color='red', linestyle='--', linewidth=2, label=f"Original Mean: {mean:.2f}")
plt.title(f"Monte Carlo Simulation (std = 20% of mean, column = '{column_title}')")
plt.xlabel("Simulated Mean")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
plt.show()

print(f"Total traffic (IDR): {np.sum(simulations)} ")
