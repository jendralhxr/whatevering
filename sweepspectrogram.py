import pandas as pd
import numpy as np
import math

plate = np.zeros((100,3000),dtype=complex)
base1 = np.zeros((100,3000),dtype=complex)
base2 = np.zeros((100,3000),dtype=complex)
base2bolt = np.zeros((100,3000),dtype=complex)
arm1 = np.zeros((100,3000),dtype=complex)
arm1bolt = np.zeros((100,3000),dtype=complex)
arm2 = np.zeros((100,3000),dtype=complex)
arm2bolt = np.zeros((100,3000),dtype=complex)
wrist = np.zeros((100,3000),dtype=complex)
finger = np.zeros((100,3000),dtype=complex)

for sweep in range(100):
    filename = str(sweep+1)+'.csv'
    print(sweep, ': ', filename, data.shape[0])
    data = pd.read_csv(filename, sep=',')
    
    for i in range(data.shape[0]):
        plate[sweep,i]= complex(data['plate-fft'][i])
        base1[sweep,i]= complex(data['base1-fft'][i])
        base2[sweep,i]= complex(data['base2-fft'][i])
        base2bolt[sweep,i]= complex(data['base2-bolt-fft'][i])
        arm1[sweep,i]= complex(data['arm1-fft'][i])
        arm1bolt[sweep,i]= complex(data['arm1-bolt-fft'][i])
        arm2bolt[sweep,i]= complex(data['arm2-bolt-fft-fft'][i])
        arm2[sweep,i]= complex(data['arm2-fft'][i])
        wrist[sweep,i]= complex(data['wrist-fft'][i])
        finger[sweep,i]= complex(data['finger-fft'][i])


nplate = np.abs(plate)
nbase1  = np.abs(base1)
nbase2  = np.abs(base2)
nbase2bolt = np.abs(base2bolt)
narm1 = np.abs(arm1)
narm1bolt = np.abs(arm1bolt)
narm2bolt = np.abs(arm2bolt)
narm2 = np.abs(arm2)
nwrist = np.abs(wrist)
nfinger = np.abs(finger)

for sweep in range(100):
    filename = str(sweep+1)+'.png'
    plt.figure(figsize=(18,6))
    plt.plot(fs, nplate[sweep,:], linewidth=2.0)
    plt.xlim(0, 250)
    plt.savefig(filename)
    plt.close



rdata= nplate
# scale
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler(with_mean=False)
scaler.fit(rdata)
ndata = scaler.transform(rdata)

##############

plt.figure()
plt.plot(fs, nfinger[0,:], linewidth=2.0)
plt.show()


t= np.linspace(1,100,100)
fs= np.linspace(0,500,3000)
plt.figure()
plt.pcolormesh(fs, t, ndata)
#plt.pcolormesh(fs, t, np.abs(plate))
#plt.pcolormesh(fs, t, np.abs(plate), shading='gouraud')
plt.colorbar()
plt.ylabel('Frequency response bin [Hz]')
plt.xlabel('Frequency sweep [Hz]')
plt.show()
plt.savefig('foo.png', bbox_inches='tight')    
    
####
for i in range(1500):
    plate[sweep,i]= complex(data['plate-fft'][i])
    base1[sweep,i]= complex(data['base1-fft'][i])
    base2[sweep,i]= complex(data['base2-fft'][i])
    base2bolt[sweep,i]= complex(data['base2-bolt-fft'][i])
    arm1[sweep,i]= complex(data['arm1-fft'][i])
    arm1bolt[sweep,i]= complex(data['arm1-bolt-fft'][i])
    arm2bolt[sweep,i]= complex(data['arm2-bolt-fft-fft'][i])
    arm2[sweep,i]= complex(data['arm2-fft'][i])
    wrist[sweep,i]= complex(data['wrist-fft'][i])
    finger[sweep,i]= complex(data['finger-fft'][i])

