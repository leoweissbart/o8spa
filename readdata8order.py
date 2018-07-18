import os
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from scipy import signal
from order8_keybits_to_HL import order8_keybits_to_HL
from order8_HL_to_keybits import order8_HL_to_keybits
from patternClassification8 import patternClassification8_6patterns
from correlation_vs_model8 import correlation_vs_model8_6patterns
from printHex256bits import printHex256bits
from scipy.interpolate import interp1d
import time

tdebut=time.time()

# #the unknown
# #t=time
# #x=power consuption
# #y=trigger
unknown_raw_power = pd.read_csv('mesures/ecc_order8_256_avg64_lowpt.csv',header=21,names = ('t','x'))
unknown_raw_trigger = pd.read_csv('mesures/ecc_order8_256_avg64_lowpt_trig.csv',header=21,names = ('t','y'))
#for model
#t=time
#x=power consuption
#y=ladderstep
model_raw_power = pd.read_csv('mesures/ecc_order8_256_avg64_date2.csv',header=21,names = ('t','x'))
model_raw_trigger = pd.read_csv('mesures/ecc_order8_256_avg64_date2_trig.csv',header=21,names = ('t','y'))


debut= time.time()
#if the sampling frequency of testing dataset is lower than the one for training dataset, we should do an interpolation to match the total number of points
#we create interpolation for power and trigger so the data is the same size as training data (we lose time information)
t_interpolate=np.linspace(unknown_raw_power.t.iloc[0],unknown_raw_power.t.iloc[-1],len(model_raw_power.t))#same time array as unknown raw power but with the number of point of model raw power
f_power=interp1d(unknown_raw_power.t,unknown_raw_power.x,kind='cubic')
f_trigger=interp1d(unknown_raw_power.t,unknown_raw_trigger.y)
unknwon_inter_power=f_power(t_interpolate)#interpolation of power trace of unknown attack
unknown_inter_trigger=f_trigger(t_interpolate)#interpolation of trigger trace of unknwon attack
fin= time.time()
print("interpolation time : ",fin-debut)

# unknown_raw_data.u-=3
plt.figure()
plt.title('Test set')
plt.plot(t_interpolate,unknwon_inter_power,t_interpolate,unknown_inter_trigger)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Trigger'),loc='best')
# model_raw_data.x-=0.3
plt.figure()
plt.title('Model raw data')
plt.plot(model_raw_power.t,model_raw_power.x,model_raw_trigger.t,model_raw_trigger.y,linewidth=0.5)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')


debut=time.time()
#recover keybits from training data
with open('mesures/avg64_date2_keybits_bin.txt') as f:
    keybits = f.read().splitlines()
keybits = [int(i) for i in keybits]
fin=time.time()
print("convert keybits for training set time = ",fin-debut,"s")

debut=time.time()
#transform the 0 and 1 of bit key into high and low levels of trace for X and Z and take one to class the patterns
predicted_level_x,predicted_level_z,pat=order8_keybits_to_HL(keybits)
fin=time.time()
print("convert into patterns time = ",fin-debut,"s")

#cut the measure in pattern according to the signal (supervised)
debut=time.time()
patternA,patternB,patternC=patternClassification8_6patterns(model_raw_power.x,model_raw_trigger.y,predicted_level_x,predicted_level_z)
fin=time.time()
print("classification time for training data time = ",fin-debut,"s")

debut=time.time()
model=[[],[],[],[],[],[]]
colors=['k','g','r','y','b','m','c','y']
for j,ind in enumerate([patternA[0],patternA[1],patternB[0],patternB[1],patternC[0],patternC[1]]):
    for i in range(len(ind)):
        ind[i]-=np.mean(ind[i])
    t=np.linspace(0,len(ind[0])-1,len(ind[0]))
    icolors=0
    name=['A1','A2','B1','B2','C1','C2']
    plt.figure()
    plt.title(name[j])
    for i in range(len(ind)):
        icolors=(i%5)
        plt.plot(t,ind[i],colors[icolors])
    model[j]=np.mean(ind,axis=0)
    model[j]=(model[j]-np.mean(model[j]))/(np.std(model[j]))
#print all model
plt.figure()
plt.title('Model A1,A2,B1,B2,C1,C2')
for i in range(len(model)):
    t=np.linspace(0,(len(model[i])-1)*1e-4,len(model[i]))
    plt.plot(t,model[i])
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('A1','A2','B1','B2','C1','C2'),loc='best')
fin=time.time()
print("creating models from samples = ",fin-debut,"s")

#this is the key bits values we should retreive considering the one used for unknown measure (to verify we retreive the good key)
with open('mesures/avg64_lowpt_keybits_bin.txt') as f:
    predicted_keybits = f.read().splitlines()
predicted_keybits = [int(i) for i in predicted_keybits]

predicted_unknown_level_x,predicted_unknown_level_z,pre_pattern=order8_keybits_to_HL(predicted_keybits)

#we do correlation
debut=time.time()
unknown_xlevel,unknown_zlevel,u_pattern = correlation_vs_model8_6patterns(unknwon_inter_power,unknown_inter_trigger,model)
fin=time.time()
print("correlation time = ",fin-debut,"s")

# #and convert the levels into keybits with order 4 point algorithm
unknown_keybits=order8_HL_to_keybits(unknown_xlevel,unknown_zlevel)

if unknown_keybits==predicted_keybits:
    print('Victory')
    printHex256bits(predicted_keybits)
else:
    print('unknown level/predicted level\n')
    print(pre_pattern)
    print(u_pattern)
    print('unknown key/predicted key\n')
    print(unknown_keybits)
    print(predicted_keybits)
    
tfin=time.time()
print("total time = ",tfin-tdebut," s")

plt.show()