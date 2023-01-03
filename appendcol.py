#use it like:
#  for i in *csv; do python -u appendcol.py out.csv $i; done

import pandas as pd
import sys

path = sys.argv[1]
output = pd.read_csv(sys.argv[1])
source = pd.read_csv(sys.argv[2])
output = pd.concat([output, source['33_vx']], axis=1)
output.rename(columns={'33_vx':source})
output.to_csv(sys.argv[1])
