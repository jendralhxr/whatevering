# how to use:
# python -u fftbatch.py INPUT.CSV OUTPUT.CSV
# 
# make sure the input CSV file looks like:
# 
# 0x,0y,1x,1y,2x,2y,3x,3y,4x,4y,5x,5y,6x,6y
# -0.156801735,0.033471026,-0.024464402,-0.019356534,-0.029520272,-0.029231801,-0.011195623,-0.026114705,0.419329577,0.008497488,-0.059557693,0.003096246,-0.080551202,-0.005404813
# -0.12964305,-0.000295031,-0.00466432,0.005531404,-0.021611498,-0.021471175,-0.053258048,-0.021698398,0.353111103,0.034661752,-0.15548303,0.023373402,-0.159337898,-0.006482599
# ....
# -0.132763715,0.010521176,-0.017745339,0.001147315,-0.026792285,-0.040743305,-0.074743752,0.000280353,0.300701637,0.010709082,-0.182083589,0.016817207,-0.17127529,-0.022749733

import pandas as pd
import sys

source = pd.read_csv(sys.argv[1])
output= source

for i in ["0x","1x","2x","3x","4x","5x","6x"]:
    # may need to scale according to the number of samples
    output[i]= np.fft.fft(source[i])

output.to_csv(sys.argv[2], index=False)