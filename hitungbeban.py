import numpy as np
import pandas as pd

df = pd.read_csv('edges2.csv')
targets = df['target'].unique()
rand_values = pd.Series(np.random.rand(len(targets)), index=targets)

# Compute weighted values
df['rand_val'] = df['target'].map(rand_values)
df['weighted_val'] = df['rand_val'] * df['weight']

# Aggregate the result by source
result = df.groupby('source')['weighted_val'].sum()

# Display the results
print(result.sort_values(ascending=False))
