
import numpy as np
import matplotlib.pyplot as plt

# Define the x range for the circle
x = np.linspace(0, 2, 400)  # From 0 to 2

# Define the upper and lower bounds for y
y_upper = 1 + np.sqrt(1 - (x - 1)**2) # Upper semicircle
y_lower = 1 - np.sqrt(1 - (x - 1)**2)  # Lower semicircle

# Plot the circle and fill the area
plt.figure(dpi=300)
plt.figure(figsize=(6, 6))
#plt.fill_between(x, y_lower, y_upper, color='blue', alpha=0.5)  # Fill the circle
x = np.linspace(0, 2, 500)  # 500 points between 0 and 2
y = np.sin(3 * np.pi * x) + 0.5 * np.cos(5 * np.pi * x) - 0.2 * np.sin(7 * np.pi * x)

import numpy as np
import matplotlib.pyplot as plt

# Generate x values
x = np.linspace(0, 2, 500)

# Parameters for three normal distributions
params = [
    {"mean": 0.5, "std": 0.1, "color": "blue", "label": r"$\mu=0.5, \sigma=0.1$"},
    {"mean": 1.0, "std": 0.2, "color": "green", "label": r"$\mu=1.0, \sigma=0.2$"},
    {"mean": 1.5, "std": 0.3, "color": "red", "label": r"$\mu=1.5, \sigma=0.3$"},
]

# Plot each distribution
plt.figure(figsize=(8, 6))
for param in params:
    mean = param["mean"]
    std = param["std"]
    color = param["color"]
    label = param["label"]
    y = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)
    plt.plot(x, y, color=color, label=label)

# Customize the plot
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.xlim(0, 2)
plt.ylim(0, 5)
plt.grid(True)
plt.ylabel('Probability Density')
plt.legend()

plt.plot(x, y, color='blue')
plt.plot(x, y_upper, color='black')  # Upper boundary of the circle
plt.plot(x, y_lower, color='black')  # Lower boundary of the circle
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)



# Set the axis limits and ticks
plt.gca().set_aspect('equal', adjustable='box')
plt.xticks(np.arange(0, 2.1, 0.25))  # Set x-axis ticks from 0 to 2 with step 0.5
plt.yticks(np.arange(0, 2.1, 0.25))  # Set y-axis ticks from 0 to 2 with step 0.5
plt.xlim(0, 2)
plt.ylim(0, 2)

# Add legend and labels
plt.legend()
plt.title('Lingkaran: $(x-1)^2 + (y-1)^2 = 1$')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()


x_min= 0
x_max= 2
y_min= 0
y_max= 2

num_samples= 100000
res= np.zeros(10)
for n in range(10):
    xr = np.random.uniform(0, x_max-x_min, num_samples)
    yr = np.random.uniform(0, y_max-y_min, num_samples)
    
    inside= 0
    for i in range(len(xr)):
        r= (xr[i]-1)**2 + (yr[i]-1)**2
        if r<=1:
            inside += 1
    res[n]= inside/num_samples *4

mean_x = np.mean(res)
std_dev_x = np.std(res)
print(f"{mean_x:.10f} ± {std_dev_x:.6f}")

# Define the range for num_samples (logarithmic scale)
sample_sizes = [int(10**i) for i in range(1, 9)]  # 10 to 1e7
means = []
std_devs = []

for num_samples in sample_sizes:
    res = np.zeros(10)
    for n in range(10):
        # Generate random samples
        xr = np.random.uniform(0, 2, num_samples)
        yr = np.random.uniform(0, 2, num_samples)
        
        # Compute the squared distances in a vectorized way
        r = (xr - 1)**2 + (yr - 1)**2
        
        # Count points inside the circle
        inside = np.sum(r <= 1)
        res[n] = inside / num_samples * 4
    means.append(np.mean(res))
    std_devs.append(np.std(res))

# Plotting the results
plt.figure(figsize=(10, 6))
plt.errorbar(sample_sizes, means, yerr=std_devs, fmt='o', capsize=5, label="Estimate ± Std Dev")
plt.xscale('log')
plt.xlabel("Jumlah sampel ")
plt.ylabel("Hasil pi")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()

