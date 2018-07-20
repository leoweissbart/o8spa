import os
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from scipy import signal
from order8_keybits_to_HL import order8_keybits_to_HL
from order8_HL_to_keybits import order8_HL_to_keybits
from patternClassification8 import patternClassification8_v3
from correlation_vs_model8 import correlation_vs_model8_6patterns_real
from printHex256bits import printHex256bits
import time

debut=time.time()

def butter_lowpass_filter(data,cut_freq, fs, order=5):
    nyq = 0.5 * fs
    cut_freq = cut_freq / nyq
    b,a=signal.butter(order,cut_freq,btype='lowpass')
    y = signal.lfilter(b, a, data)
    return y

# #the unknown
# #t=time
# #x=power consuption
# #u=trigger
unknown_raw_data = pd.read_csv('mesure-order8-5-10-18/Order8average50total01unknown.csv',header=23,names = ('t','x','u'))

# unknown_raw_data.u-=3
plt.figure()
plt.title('Test set')
plt.plot(unknown_raw_data.t,unknown_raw_data.x,unknown_raw_data.t,unknown_raw_data.u)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Trigger'),loc='best')
# plt.show()

#for model
#t=time
#x=power consuption
#u=trigger            (not used)
#y=ladderstep
#z=bitvalue           (not used)
model_raw_data = pd.read_csv('mesure-order8-5-9-18/Order8average50total01.csv',header=23,names = ('t','x','u','y'))


model_raw_data.x-=0.3
plt.figure()
plt.title('Model raw data')
plt.plot(model_raw_data.t,model_raw_data.x,model_raw_data.t,model_raw_data.y,linewidth=0.5)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')

fs=1e4
cutoff_hz=1250
unknown_filtered_x=butter_lowpass_filter(unknown_raw_data.x,cutoff_hz,fs)
unknown_filtered_trigger=butter_lowpass_filter(unknown_raw_data.u,cutoff_hz,fs)
plt.figure()
plt.title('Unknown filtered data')
plt.plot(unknown_raw_data.t,unknown_filtered_x,unknown_raw_data.t,unknown_filtered_trigger)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Trigger'),loc='best')



#filter the mesure and replace its value in the data_frame
model_filtered_x=butter_lowpass_filter(model_raw_data.x,cutoff_hz,fs)
model_filtered_y=butter_lowpass_filter(model_raw_data.y,cutoff_hz,fs)

plt.figure()
plt.title('Training set')
plt.plot(model_raw_data.t,model_filtered_x,model_raw_data.t,model_filtered_y)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')



#recover keybits from training data
with open('mesure-order8-5-9-18/bin_key_unknown.txt') as f:
    keybits = f.read().splitlines()
keybits = [int(i) for i in keybits]


#transform the 0 and 1 of bit key into high and low levels of trace for X and Z and take one to class the patterns
predicted_level_x,predicted_level_z,pat=order8_keybits_to_HL(keybits)

#############################################################################################################################
patternA,patternB,patternC=patternClassification8_v3(model_filtered_x,model_filtered_y,predicted_level_x,predicted_level_z)

model=[[],[],[],[],[],[]]
colors=['k','g','r','y','b','m','c','y']
for j,ind in enumerate([patternA[0],patternA[1],patternB[0],patternB[1],patternC[0],patternC[1]]):
    for i in range(len(ind)):
        ind[i]-=np.mean(ind[i])
    # t=np.linspace(0,len(ind[0])-1,len(ind[0]))
    # j=0
    # plt.figure()
    # for i in range(len(ind)):
    #     j=(i%5)
    #     plt.plot(t,ind[i],colors[j])
    #     plt.title(i)
    model[j]=np.mean(ind,axis=0)
    model[j]=(model[j]-np.mean(model[j]))/(np.std(model[j]))

#print all model

plt.figure()
plt.title('Model A1,A2,B1,B2,C1,C2')
for i in range(len(model)):
    t=np.linspace(0,(len(model[i])-1)*1e-4,len(model[i]))
    plt.plot(t,model[i],colors[i])
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('A1','A2','B1','B2','C1','C2'),loc='best')


#############################################################################################################################

#this is the key bits values we should retreive considering the one used for unknown measure (to verify we retreive the good key)
with open('mesure-order8-5-10-18/bin_unknown_keybits01u.txt') as f:
    predicted_keybits = f.read().splitlines()
predicted_keybits = [int(i) for i in predicted_keybits]

predicted_unknown_level_x,predicted_unknown_level_z,pre_pattern=order8_keybits_to_HL(predicted_keybits)
# print(pre_pattern)

#############################################################################################################################################
#we do correlation using 6 patterns
unknown_xlevel,unknown_zlevel,u_pattern = correlation_vs_model8_6patterns_real(unknown_filtered_x,unknown_filtered_trigger,model)


#############################################################################################################################################

# #and convert the levels into keybits with order 4 point algorithm
unknown_keybits=order8_HL_to_keybits(unknown_xlevel,unknown_zlevel)



if unknown_keybits==predicted_keybits:
    print('Victory')
    printHex256bits(predicted_keybits)
else:
    print('unknown level/predicted level\n')
    print(unknown_xlevel)
    print(predicted_unknown_level_x)
    print('\n')
    print(unknown_zlevel)
    print(predicted_unknown_level_z)
    print('unknown key/predicted key\n')
    print(unknown_keybits)
    print(predicted_keybits)
    
fin=time.time()

print("time = ",fin-debut," s")

plt.show()