import os
import pandas
import matplotlib.pyplot as plt
from scipy.signal import medfilt

os.chdir("D:\\csv_5_8\\")
poc1= pandas.read_csv("1.csv")
time= poc1["framenum"]
platex= poc1["plate_x"]

plt.plot(time, platex_filtered)

platex_filtered= medfilt(platex, 3)
poc1["plate_x"]= platex_filtered
# or you can also do it like
poc1["base_x"]= medfilt(poc1["base_x"], 3)
# repeat for all other parts

poc1.to_csv("test.csv")
