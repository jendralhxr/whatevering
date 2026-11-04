import matplotlib.pyplot as plt
import pandas as pd

# Load datasets
df_masked = pd.read_csv('3651masked.csv', skiprows=1, on_bad_lines='skip')
df_bersih = pd.read_csv('3651bersih.csv', skiprows=1, on_bad_lines='skip')

# Clean numeric data
for df in [df_masked, df_bersih]:
    df['time'] = pd.to_numeric(df['time'], errors='coerce')
    df['count'] = pd.to_numeric(df['count'], errors='coerce')
    df['threshold'] = pd.to_numeric(df['threshold'], errors='coerce')
    df.dropna(subset=['time', 'count', 'threshold'], inplace=True)

window_size = 60

# Apply 60-sample moving average smoothing
df_masked['count_smooth'] = (
    df_masked['count'].rolling(window=window_size, min_periods=1).mean()
)
df_masked['thresh_smooth'] = (
    df_masked['threshold'].rolling(window=window_size, min_periods=1).mean()
)

df_bersih['count_smooth'] = (
    df_bersih['count'].rolling(window=window_size, min_periods=1).mean()
)
df_bersih['thresh_smooth'] = (
    df_bersih['threshold'].rolling(window=window_size, min_periods=1).mean()
)

# Create single plot with secondary y-axis
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

# 3651 masked: cell count (solid red), threshold (dashed fainter red)
ax1.plot(
    df_masked['time'],
    df_masked['count_smooth'],
    label='3651 masked (cellcount)',
    color='#d62728',
    linewidth=1.5,
    alpha=0.9,
)
ax2.plot(
    df_masked['time'],
    df_masked['thresh_smooth'],
    label='3651 masked (threshold)',
    color='#d62728',
    linewidth=1.5,
    alpha=0.35,
    linestyle='--',
)

# 3651 bersih: cell count (solid blue), threshold (dashed fainter blue)
ax1.plot(
    df_bersih['time'],
    df_bersih['count_smooth'],
    label='3651 bersih (cellcount)',
    color='#1f77b4',
    linewidth=1.5,
    alpha=0.9,
)
ax2.plot(
    df_bersih['time'],
    df_bersih['thresh_smooth'],
    label='3651 bersih (threshold)',
    color='#1f77b4',
    linewidth=1.5,
    alpha=0.35,
    linestyle='--',
)

# Formatting
ax1.set_xlabel('Time (s)', fontsize=12)
ax1.set_ylabel('Cell Count', fontsize=12)
ax2.set_ylabel('Threshold (dashed / fainter)', fontsize=12)
plt.title(
    '3651 Masked vs Bersih: Time vs Cell Count and Threshold',
    fontsize=14,
    fontweight='bold',
)
ax1.grid(True, linestyle=':', alpha=0.6)

# Combine legends from both y-axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig('3651_masked_vs_bersih_single_plot.png', dpi=300)
plt.show()