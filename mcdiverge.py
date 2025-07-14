import pandas as pd
import numpy as np
from datetime import datetime

seed = int(datetime.now().timestamp())  # Seconds since epoch
np.random.seed(seed)

goods_mean = 1008.5
goods_std = 0.20 * goods_mean  # 20% standard deviation
goods_2028 = np.random.normal(loc=goods_mean, scale=goods_std)


#------- benefit 
initial_data = {
    'year': [2028],
    'goods': goods_2028,
    'boats': [159.8],
    'vacation': [881.6],
}

df_benefit = pd.DataFrame(initial_data)
df_benefit['total'] = df_benefit['goods'] + df_benefit['boats'] + df_benefit['vacation']

# Growth rates
growth_rates = {
    'goods': 0.05,      # 5% annual growth
    'boats': 0.02,      # 2% annual growth
    'inflation': 0.038    
}

# Project data through to 2047
for year in range(2029, 2048):
    prev = df_benefit.iloc[-1]
    new_goods = prev['goods'] * (1 + growth_rates['goods']) * (1 + growth_rates['inflation'])
    new_boats = prev['boats'] * (1 + growth_rates['boats'])
    new_vacation = prev['vacation']  * (1 + growth_rates['goods']) * (1 + growth_rates['inflation'])
    new_total = new_goods + new_boats + new_vacation

    df_benefit = pd.concat([df_benefit, pd.DataFrame([{
        'year': year,
        'goods': new_goods,
        'boats': new_boats,
        'vacation': new_vacation,
        'total': new_total
    }])], ignore_index=True)

# Optional: format floats for better display
pd.options.display.float_format = '{:,.2f}'.format

# Print full result
#print(df_benefit)


#---------- costs



# Define capex range
capex_min = 23947.4
capex_max = 28736.8
cost_overrun = capex_max - capex_min # this is cost overrun

# Random capex for 2027
# capex_2027 = capex_min + np.random.rand() * cost_overrun # uniform distribution

# Compute capex_2027 using the normal random ratio
mean_ratio = 0.5      # mid of 0–1
std_ratio = 0.2       # 20% std deviation
random_ratio = np.random.normal(loc=mean_ratio, scale=std_ratio)
random_ratio = np.clip(random_ratio, 0, 1)
capex_2027 = capex_min + random_ratio * cost_overrun

opex_2027 = 494.5
total_2027 = capex_2027 + opex_2027

# Create the initial DataFrame for 2027
df_cost = pd.DataFrame([{
    'year': 2027,
    'capex': capex_2027,
    'opex': opex_2027,
    'total': total_2027
}])

# Set opex growth rate
opex_growth = 0.01

# Generate data from 2028 to 2047
for year in range(2028, 2048):
    prev = df_cost.iloc[-1]
    new_opex = prev['opex'] * (1 + opex_growth)
    new_capex = 0
    new_total = new_capex + new_opex

    df_cost = pd.concat([df_cost, pd.DataFrame([{
        'year': year,
        'capex': new_capex,
        'opex': new_opex,
        'total': new_total
    }])], ignore_index=True)

# Optional: nicer float formatting
pd.options.display.float_format = '{:,.2f}'.format

# Print the resulting DataFrame
print(df_cost)

#---- PV
#base_year= 2027
base_year = df_benefit['year'].iloc[0]

discount_rate= 0.1

df_benefit['perceived_value'] = df_benefit['total'] * ((1-discount_rate) ** (df_benefit['year'] - base_year))

base_year = df_cost['year'].iloc[0]
df_cost['perceived_value'] = df_cost['total'] * (0.9 ** (df_cost['year'] - base_year))



