import pandas as pd
import sys
 
# Set path to CSV files 
path = sys.argv[1])
 
# Read CSV file into DataFrame 
output = pd.read_csv(sys.argv[1])) 
source = pd.read_csv(sys.argv[2])) 
 
# Transfer column 'x' from df1 to df2 
output = pd.concat([output, source['33_vx']], axis=1) 
output.rename(columns={'33_vx':source})

# Save df2 as CSV 
output.to_csv(sys.argv[1])