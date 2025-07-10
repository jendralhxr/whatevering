import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv('traffic.csv')  # replace with your actual filename
column_title= 'total'
data = df[column_title].dropna().values  # drop NaNs if any
n_simulations= int(1e3)
element_std = 0.20 * data

# Simulate each data point independently using its own mean/std
simulations = np.random.normal(loc=data, scale=element_std, size=(n_simulations, len(data)))

data_safe = np.where(data == 0, np.nan, data)  # or use a small epsilon if preferred
simulated_ratios = simulations / data_safe  # shape: (1000, len(data))
mean_ratios = np.nanmean(simulated_ratios, axis=1)  # handle NaNs safely

# the plot
years = df['year'].values
np.random.seed(42)  # for reproducibility
selected_indices = np.random.choice(simulations.shape[0], size=20, replace=False)
selected_simulations = simulations[selected_indices]

plt.figure(figsize=(12, 6))
plt.plot(years, data, color='darkblue', linewidth=2, label='Original Data')

# Generate 20 light random colors and plot simulations
for sim in selected_simulations:
    # Light random color
    light_color = np.random.rand(3) * 0.5 + 0.5  # RGB values between 0.5 and 1.0
    plt.plot(years, sim, color=light_color, linewidth=1, alpha=0.7)

# Labels and legend
plt.title("Original Data and 20 Monte Carlo Simulations (20 is for illustation purpose only)")
plt.xlabel("Year")
plt.ylabel(f"{column_title}")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# # mungkin agak susah dicerna
# plt.hist(simulated_ratios, bins=30)
# plt.axhline(1.0, color='red', linestyle='--', linewidth=2, label="Original (ratio = 1)")
# plt.title(f"Monte Carlo Simulation (Ratio: simulated / {column_title})")
# plt.xlabel("Mean Ratio per Simulation")
# plt.ylabel("Frequency")
# plt.legend()
# plt.grid(True)
# plt.show()


print(f"Total traffic (IDR): {np.sum(simulations)/n_simulations} ")
