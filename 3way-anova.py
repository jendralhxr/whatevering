import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the processed data
df = pd.read_csv('compound_measurements.csv')

# Ensure factors are categorical
df['compound'] = df['compound'].astype('category')
df['method'] = df['method'].astype('category')
df['time'] = df['time'].astype('category')

# Fit the 3-way ANOVA model (including all interactions)
model = ols('value ~ C(compound) * C(time) * C(method)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

print("3-Way ANOVA Results:")
print(anova_table)

