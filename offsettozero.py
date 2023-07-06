# use this script like:
# python offsetzero.py $$.csv
# 
# for multiple batch files
#    for i in `seq 1 100`; do python offsetzero.py "$i".csv; done # linux
#    for /l %b in (1,1,100) do python offsetzero.py %b.csv; done # windows

import pandas as pd
import sys

tee = pd.read_csv("22.csv")

for i in range(1, len(tee.columns)): # from 2nd to last colum
    colname= "%s_offset" % tee.columns[i]
    average= tee.iloc[:,i].mean(axis= None);
    tee.insert(len(tee.columns), colname, tee.iloc[:,i]-average)
    
tee.to_csv(sys.argv[1], index=False)
