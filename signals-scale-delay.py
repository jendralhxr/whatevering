# inspired from:
# https://stats.stackexchange.com/questions/541277/how-can-i-get-the-phase-difference-between-two-frequencies
# https://stackoverflow.com/questions/69117617/how-to-find-the-lag-between-two-time-series-using-cross-correlation

import numpy as np
import math

nsr = 0
r = np.random.normal(size=(3000,2)) * nsr
#phdiff = math.pi
phdiff = math.pi/ 2
omega = 11
t = np.arange(3000) / 500
rdata = np.zeros((len(t), 2))
ph0 = 2 * math.pi * np.random.uniform()
rdata[:,0] = np.sin(2 * math.pi * omega * t + ph0)
rdata[:,1] = np.sin(2 * math.pi * omega * t + phdiff + ph0)
rdata = rdata + r

# scale
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(rdata)
data = scaler.transform(rdata)

import matplotlib.pyplot as plt
#plt.figure()
#plt.plot(data[1:500,:])
#plt.show()

# phase difference determination
#plt.figure(figsize=(4,4))
#plt.title('Phase diagram')
#plt.scatter(data[1:100,0],data[1:100,1])
#plt.show()

#c = np.cov(np.transpose(data))
#print('cov: ', c)
#phi = np.arccos(c[0,1] )
#print('true phase diff (radians):', phdiff, '\t(degrees):', phdiff / (2 * math.pi) * 360)
#print('phase estimate (radians): ', phi, '(degrees): ', phi / math.pi * 180)

correlation = signal.correlate(data[:,0], data[:,1], mode="same", method=' direct')
lags = signal.correlation_lags(len(x), len(y), mode="same")
lag = lags[np.argmax(abs(correlation))]
print('lag ', lag, 'elem')

#plt.figure()
#plt.plot(lags)
#plt.show()
