#use it like:
#  for i in *csv; do python -u appendcol.py compiled.csvx $i; done

import pandas as pd
import sys

path = sys.argv[1]
output = pd.read_csv(sys.argv[1])
source = pd.read_csv(sys.argv[2])
temp= value=source['33_vx']
output.insert(loc=len(output.columns), column=sys.argv[2], value=temp)
output.to_csv(sys.argv[1], index=False)
