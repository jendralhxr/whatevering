import pandas as pd
import numpy as np
from datetime import datetime

seed = int(datetime.now().timestamp())  # Seconds since epoch
np.random.seed(seed)

iter_max= int(1e4)

netpv = np.linspace(0.0, 0, iter_max)

for i in range(iter_max):

    #------- benefit 
    
    goods_mean = 336.0
    goods_std = 0.20 * goods_mean  # 20% standard deviation
    goods_2028 = np.random.normal(loc=goods_mean, scale=goods_std)
    
    overestimate_mean = 59.8
    overestimate_std = 276  
    overestimate = np.random.normal(loc=overestimate_mean, scale=overestimate_std)
        
    initial_data = {
        'year': [2028],
        'goods': goods_2028,
        'boats': [0],
        'vacation': [293.0],
    }
    
    df_benefit = pd.DataFrame(initial_data)
    df_benefit['total'] = df_benefit['goods'] + df_benefit['boats'] + df_benefit['vacation']
    
    # Growth rates
    growth_rates = {
        'goods': 0.04,      # 5% annual growth
        'boats': 0.02,      # 2% annual growth
        'inflation': 0.038    
    }
    
    # Project data through to 2047
    for year in range(2029, 2048):
        prev = df_benefit.iloc[-1]
        new_goods = prev['goods'] * (1 + growth_rates['goods']) * (1 + growth_rates['inflation'])
        new_boats = prev['boats'] * (1 + growth_rates['boats'])
        new_vacation = prev['vacation']  * (1 + growth_rates['goods']) * (1 + growth_rates['inflation'])
        new_total = new_goods + new_boats + new_vacation -overestimate
    
        df_benefit = pd.concat([df_benefit, pd.DataFrame([{
            'year': year,
            'goods': new_goods,
            'boats': new_boats,
            'vacation': new_vacation,
            'total': new_total
        }])], ignore_index=True)
    
    # pd.options.display.float_format = '{:,.2f}'.format
    # print(df_benefit)
    
    
    #---------- costs
    
    # Define capex range
    capex_base= 3370.0
    
    # overrun cost follow normal distribution
    # Flyvbjerg 2003, Transport reviews 23.1 (2003): 71-88.
    overrun_mean= 0.646 * capex_base
    overrun_stddev= 0.495 * capex_base
    overrun = np.random.normal(loc=overrun_mean, scale=overrun_stddev)

    # random_ratio = np.random.normal(loc=mean_ratio, scale=std_ratio)
    # random_ratio = np.clip(random_ratio, 0, 1)
    capex_2027 = capex_base + overrun
    
    opex_ratio= 0.0206498336269329
    opex_2027 = opex_ratio * capex_2027
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
    
    # pd.options.display.float_format = '{:,.2f}'.format
    # print(df_cost)
    
    
    #---- PV
    # empirical evidence, Ramsey formula,
    # https://www.pc.gov.au/research/supporting/cost-benefit-discount/cost-benefit-discount.pdf
    discount_rate = np.random.normal(loc=(11-0.24)/2, scale=1.793)  # loc = mean, scale = std
    discount_rate = np.clip(discount_rate, 0.24, 11) / 100
    
    # our gut feeling
    # discount_rate = np.random.normal(loc=0.1, scale=0.04)
    # discount_rate = np.clip(discount_rate, 0, 1)  # ensure valid %
    base_year = df_benefit['year'].iloc[0]
    df_benefit['perceived_value'] = df_benefit['total'] * ((1-discount_rate) ** (df_benefit['year'] - base_year))
    
    base_year = df_cost['year'].iloc[0]
    df_cost['perceived_value'] = df_cost['total'] * ((1-discount_rate) ** (df_cost['year'] - base_year))
    
    netpv[i]= df_benefit['perceived_value'].sum() - df_cost['perceived_value'].sum()

# visualization for some discussion
    
import matplotlib.pyplot as plt
from scipy.stats import norm

# Fit normal distribution to the NPV
mu, std = norm.fit(netpv)
plt.hist(netpv, bins=30, density=True, color='skyblue', edgecolor='black', alpha=0.7)

xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 1000)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'r', linewidth=2, label=f'N({mu:.2f} ±{std:.2f})')
plt.title(f'Expected Cumulative NPV from Monte Carlo Simulation (n={iter_max})')
plt.xlabel('20-year NPV (million IDR)')
plt.ylabel('Probability Density')
plt.legend()
  
profit= (netpv > 0).sum() # playing fair
# profit= (netpv > 0).sum() # if expecting some kind of return already
loss = iter_max - profit

print(f"turns profit: {profit}")
print(f"incur losses: {loss}")

cumsum_untung = netpv[netpv > 0].cumsum().sum()
cumsum_rugi = netpv[netpv < 0].cumsum().sum()

print(f"cumsum: {cumsum_untung+cumsum_rugi}")


# confidence interval
from scipy import stats

n = len(netpv)
mean = np.mean(netpv)
std_err = stats.sem(netpv)  # Standard error of the mean

# 95% confidence interval
confidence = 0.95
h = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)

ci_lower = mean - h
ci_upper = mean + h

print(f"Mean NPV: {mean:.2f}")
print(f"95% Confidence Interval: ({ci_lower:.2f}, {ci_upper:.2f})")