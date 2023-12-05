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

#--------------

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

r2d = 180.0/np.pi   # conversion factor RAD-to-DEG
delta_phi_true = 50.0/r2d

def detect_phase_shift(t, x, y):
    '''detect phase shift between two signals from cross correlation maximum'''
    N = len(t)
    L = t[-1] - t[0]
    
    cc = signal.correlate(x, y, mode="same")
    i_max = np.argmax(cc)
    phi_shift = np.linspace(-0.5*L, 0.5*L , N)
    delta_phi = phi_shift[i_max]

    print("true delta phi = {} DEG".format(delta_phi_true*r2d))
    print("detected delta phi = {} DEG".format(delta_phi*r2d))
    print("error = {} DEG    resolution for comparison dphi = {} DEG".format((delta_phi-delta_phi_true)*r2d, dphi*r2d))
    print("ratio = {}".format(delta_phi/delta_phi_true))
    return delta_phi


L = np.pi*10+2     # interval length [RAD], for generality not multiple period
N = 1001   # interval division, odd number is better (center is integer)
noise_intensity = 0.0
X = 0.5   # amplitude of first signal..
Y = 2.0   # ..and second signal

phi = np.linspace(0, L, N)
dphi = phi[1] - phi[0]

'''generate signals'''
nx = noise_intensity*np.random.randn(N)*np.sqrt(dphi)   
ny = noise_intensity*np.random.randn(N)*np.sqrt(dphi)
x_raw = X*np.sin(phi) + nx
y_raw = Y*np.sin(phi+delta_phi_true) + ny

'''preprocessing signals'''
x = x_raw.copy() 
y = y_raw.copy()
#window = signal.windows.hann(N)   # Hanning window 
x -= np.mean(x)   # zero mean
y -= np.mean(y)   # zero mean
#x /= np.std(x)    # scale
#y /= np.std(y)    # scale
#x *= window       # reduce effect of finite length 
#y *= window



       # reduce effect of finite length 

print(" -- using raw data -- ")
delta_phi_raw = detect_phase_shift(phi, x_raw, y_raw)

print(" -- using preprocessed data -- ")
delta_phi_preprocessed = detect_phase_shift(phi, x, y)
