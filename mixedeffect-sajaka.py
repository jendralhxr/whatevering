#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:04:42 2026

@author: rdx
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests

# 1. Reconstruct Data from Wide Format Matrix into Python Dictionary
raw_data = {
    'pre': {
        'urgensi': [10, 9, 8, 9, 9, 10, 8, 8, 9, 10, 9, 9, 10, 9, 10, 9, 9],
        'salin':   [10, 9, 8, 9, 9, 10, 8, 8, 8, 10, 8, 8, 10, 7, 10, 9, 10],
        'jaga':    [10, 7, 7, 9, 9, 10, 8, 8, 9, 10, 8, 10, 10, 8, 10, 10, 9],
        'kaji':    [10, 8, 8, 9, 10, 7, 8, 8, 9, 10, 9, 8, 10, 6, 10, 9, 9],
    },
    'post': {
        'urgensi': [None, None, None, None, None, None, 8, 9, 9, 10, 10, 10, 10, 10, None, 9, 9],
        'salin':   [None, None, None, None, None, None, 9, 9, 9, 10, 10, 9, 10, 7, None, 10, 10],
        'jaga':    [None, None, None, None, None, None, 9, 9, 9, 10, 10, 10, 10, 9, None, 10, 10],
        'kaji':    [None, None, None, None, None, None, 9, 9, 9, 10, 10, 8, 10, 10, None, 9, 10],
    }
}

# 2. Reshape into Long (Tidy) Format for Linear Mixed Models
records = []
for timepoint in ['pre', 'post']:
    for item_name in ['urgensi', 'salin', 'jaga', 'kaji']:
        scores = raw_data[timepoint][item_name]
        for subject_idx, score in enumerate(scores):
            if score is not None:  # Missing post-tests are omitted; REML handles unbalance
                records.append({
                    'subject_id': f"P{subject_idx + 1:02d}",
                    'time': timepoint,
                    'item': item_name,
                    'score': score
                })

df_long = pd.DataFrame(records)

# Convert categorical variables to explicit factors
df_long['time'] = pd.Categorical(df_long['time'], categories=['pre', 'post'])
df_long['item'] = pd.Categorical(df_long['item'], categories=['urgensi', 'salin', 'jaga', 'kaji'])

# 3. Model 1: Main Effects Model
# Random intercept per subject accounts for baseline individual differences
model_main = smf.mixedlm(
    "score ~ C(time, Treatment(reference='pre')) + C(item)", 
    df_long, 
    groups=df_long["subject_id"]
)
fit_main = model_main.fit()

# 4. Model 2: Interaction Model (Tests if score changes differ across items)
model_interaction = smf.mixedlm(
    "score ~ C(time, Treatment(reference='pre')) * C(item)", 
    df_long, 
    groups=df_long["subject_id"]
)
fit_interaction = model_interaction.fit()

# 5. Output Statistical Summaries
print("=" * 65)
print(" 1. MAIN EFFECTS MIXED MODEL SUMMARY ")
print("=" * 65)
print(fit_main.summary())

print("\n" + "=" * 65)
print(" 2. ITEM-INTERACTION MIXED MODEL SUMMARY ")
print("=" * 65)
print(fit_interaction.summary())

# Extract key metric for main time effect
time_coef = fit_main.params["C(time, Treatment(reference='pre'))[T.post]"]
time_pval = fit_main.pvalues["C(time, Treatment(reference='pre'))[T.post]"]

print("\n" + "-" * 65)
print(f"Overall Pre -> Post Effect Estimate : +{time_coef:.3f} points")
print(f"Statistical Significance (p-value)  : p = {time_pval:.5f}")
print("-" * 65)

# 6. Visualization: Estimated Means Trajectory by Item
plt.figure(figsize=(9, 5))
sns.pointplot(
    data=df_long, 
    x='item', 
    y='score', 
    hue='time', 
    dodge=0.2, 
    markers=['o', 's'], 
    linestyles=['-', '--'],
    errorbar='se', 
    capsize=0.1
)

plt.title("Pre- to Post-Test Likert Score Trajectories by Item", fontsize=12, fontweight='bold')
plt.xlabel("Survey Item", fontsize=10)
plt.ylabel("Mean Score (± SE)", fontsize=10)
plt.ylim(5, 10.5)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.legend(title="Timepoint")
plt.tight_layout()
plt.show()

### more analysis, Iterate through each aspect and run individual LMMs
aspect_results = []
aspects = ['urgensi', 'salin', 'jaga', 'kaji']

for aspect in aspects:
    df_sub = df_long[df_long['item'] == aspect].copy()
    
    # Fit individual LMM per aspect
    model = smf.mixedlm(
        "score ~ C(time, Treatment(reference='pre'))", 
        df_sub, 
        groups=df_sub["subject_id"]
    )
    fit = model.fit()
    
    # Extract statistics
    coef = fit.params["C(time, Treatment(reference='pre'))[T.post]"]
    se = fit.bse["C(time, Treatment(reference='pre'))[T.post]"]
    z_val = fit.tvalues["C(time, Treatment(reference='pre'))[T.post]"]
    p_val = fit.pvalues["C(time, Treatment(reference='pre'))[T.post]"]
    
    pre_mean = df_sub[df_sub['time'] == 'pre']['score'].mean()
    post_mean = df_sub[df_sub['time'] == 'post']['score'].mean()
    
    aspect_results.append({
        'Aspect': aspect,
        'Pre Mean': round(pre_mean, 2),
        'Post Mean': round(post_mean, 2),
        'Change (Est.)': round(coef, 3),
        'Std Error': round(se, 3),
        'z-value': round(z_val, 3),
        'p-value': p_val
    })

res_df = pd.DataFrame(aspect_results)

# 3. Apply Benjamini-Hochberg (FDR) Multiple Testing Correction
reject, p_adjusted, _, _ = multipletests(res_df['p-value'], method='fdr_bh')
res_df['p-adj (FDR)'] = p_adjusted

print(res_df.to_string(index=False))