import pandas as pd
import numpy as np

plate = np.zeros((100,1500),dtype=complex)
base1 = np.zeros((100,1500),dtype=complex)
base2 = np.zeros((100,1500),dtype=complex)
base2bolt = np.zeros((100,1500),dtype=complex)
arm1 = np.zeros((100,1500),dtype=complex)
arm1bolt = np.zeros((100,1500),dtype=complex)
arm2 = np.zeros((100,1500),dtype=complex)
arm2bolt = np.zeros((100,1500),dtype=complex)
wrist = np.zeros((100,1500),dtype=complex)
finger = np.zeros((100,1500),dtype=complex)

for sweep in range(100):
    filename = str(sweep+1)+'.csv'
    print(filename, data.shape[0])
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

t= np.linspace(1,100,100)
fs= np.linspace(1,250,1500)
plt.figure()
plt.pcolormesh(fs, t, np.abs(plate))
#plt.pcolormesh(fs, t, np.abs(plate), shading='gouraud')
plt.ylabel('Frequency response bin [Hz]')
plt.xlabel('Frequency sweep [Hz]')
plt.show()
    
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

        
    #print(x)
    
    
