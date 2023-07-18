import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

output= pd.DataFrame()
os.chdir("D://abdur//fft") # where you put the CSV files of FFT response and ratio

#column_name= "base_ratio"
#column_name= "base1_ratio"
#column_name= "arm_ratio"
#column_name= "arm1_ratio"
#column_name= "wrist_ratio"
column_name= "finger_ratio"

sweep= np.arange(1,101,1)
freq=np.arange(0,500/2,500/2996) #only half to show is okay
#output.insert(loc=len(output.columns), column="freq", value=freq)

for i in range(1,101):
    filename=str(i)+".csv"
    #print(filename)
    tee= pd.read_csv(filename)
    output.insert(loc=len(output.columns), column=str(i), value=tee[column_name])
    #print(tee.shape)

response= output.to_numpy()
response= response[0:freq.shape[0], 0:]

sweep, freq = np.meshgrid(sweep, freq)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#ax.set_ylim(0,250)
surf = ax.plot_surface(sweep, freq, response, cmap=cm.jet, linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)

# need somewat to scale the plot and "beautify it"