# use it like:
#    for i in *csv; do python -u appendcol.py compiled.csvx $i; done
# or more precisely like:
#    for i in `seq 5 100`; do python appendcol.py all.csv "$i".csv; done # linux
#    for /l %b in (1,1,100) do python appendcol.py all.csv %b.csv; done # windows
#
# how to use:
# 1) make empty CSV files for output
#   for i in 32 47 18 36 66 80 110; do echo a > point$i.csv; done
# 2) append from input files, be sure to get the correct path of the files
#   for i in `seq 5 100`; do python appendcol.py all.csv "$i".csv 33; done # linux
#   for /l %b in (1,1,100) do python appendcol.py all.csv %b.csv 33; done # windows
# 3) tidy up the output CSV files in your favorite spreadsheet editor

import pandas as pd
import sys

output = pd.read_csv(sys.argv[1])
source = pd.read_csv(sys.argv[2])
targetcol= sys.argv[3]
col= "%s_vx" % targetcol
temp=source[col]
output.insert(loc=len(output.columns), column=sys.argv[2], value=temp)
output.to_csv(sys.argv[1], index=False)
