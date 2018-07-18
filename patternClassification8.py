import numpy as np
import matplotlib.pyplot as plt
import time

#A1,A2,B1,B2,C1,C2
#A1,A2,A3,A4,B1,B2,C1,C2,C3,C4,C5,C6 fusing C1C5C6 in C1 and C2C3C4 in C2 A1A4 in A1 and A2A3 in A2
def patternClassification8_6patterns(data,trigger,xlevel,zlevel):
    patternA=[[],[]]
    patternB=[[],[]]
    patternC=[[],[]]
    cstate=1
    state=[1,2,3,4,5,6]
    m=[]#temporary trace constructed to be stored in A, B or C
    k=0
    run=1

    for i in range(len(data)):
        if trigger[i] < -2:
            m.append(data[i])

    del m[:3263]#remove the points before laddersteps. This nb have been adjusted regarding the curves obtained after patternclassification
    
    #plot m
    # tm=np.linspace(0,len(m)-1,len(m))
    # plt.figure()
    # plt.plot(tm,m)

    ladderstep=[]
    k=0#indenter to go through 256 loops of ladderstep
    j=0#indenter to capture one ladderstep in 'ladderstep'
    run=1#semaphore to separate repplishing of 'ladderstep' and the classification with respect to 'level'
    len_ladderstep=len(m)/256#the number of points for one ladderstep

    i=0
    petit=0
    while i<len(m):
        if run==1:
            if j<len_ladderstep-1:
                ladderstep.append(m[int(i)])
                j+=1
            else:
                run=0
                j=0
                petit+=0.13
        if run==0:
            run=1
            if xlevel[k]==1 and zlevel[k]==0:
                if cstate==state[0]:
                    patternA[0].append(ladderstep)
                    cstate=state[0]
                elif cstate==state[1]:
                    raise ValueError('State unreachable, please refere to order 8 algorithm')
                elif cstate==state[2]:
                    patternA[1].append(ladderstep)
                    cstate=state[3]
                elif cstate==state[3]:
                    patternA[1].append(ladderstep)
                    cstate=state[3]
                elif cstate==state[4]:
                    raise ValueError('State unreachable, please refere to order 8 algorithm')
                elif cstate==state[5]:
                    patternA[0].append(ladderstep)
                    cstate=state[0]
                else:
                    raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
            elif xlevel[k]==0 and zlevel[k]==1:
                if cstate==state[0]:
                    raise ValueError('State unreachable, please refere to order 8 algorithm')
                elif cstate==state[1]:
                    patternB[1].append(ladderstep)
                    cstate=state[2]
                elif cstate==state[2]:
                    raise ValueError('State unreachable, please refere to order 8 algorithm')
                elif cstate==state[3]:
                    raise ValueError('State unreachable, please refere to order 8 algorithm')
                elif cstate==state[4]:
                    patternB[0].append(ladderstep)
                    cstate=state[5]
                elif cstate==state[5]:
                    raise ValueError('State unreachable, please refere to order 8 algorithm')
                else:
                    raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
            elif xlevel[k]==1 and zlevel[k]==1:
                if cstate==state[0]:
                    patternC[0].append(ladderstep)
                    cstate=state[1]
                elif cstate==state[1]:
                    patternC[1].append(ladderstep)
                    cstate=state[4]
                elif cstate==state[2]:
                    patternC[1].append(ladderstep)
                    cstate=state[4]
                elif cstate==state[3]:
                    patternC[1].append(ladderstep)
                    cstate=state[4]
                elif cstate==state[4]:
                    patternC[0].append(ladderstep)
                    cstate=state[1]
                elif cstate==state[5]:
                    patternC[0].append(ladderstep)
                    cstate=state[1]
                else:
                    raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
            else:
                raise ValueError('The values of level should be 0s or 1s. (check if zlevel and xlevel are not both 0 for same i)')
            # t=np.linspace(0,len(ladderstep)-1,len(ladderstep))
            # print(xlevel[k],zlevel[k])
            # plt.figure()
            # plt.title(k)
            # plt.plot(t,ladderstep)
            # plt.show()
            ladderstep=[]
            k+=1
        i+=1+petit
        petit=0
    
    if k<256:#important if the last ladderstep is shorter than len_ladderstep else we would lost the last bit
        meanm=np.mean(ladderstep)
        while len(ladderstep)<len_ladderstep-1:#artifficial padding with the mean value of the signal but the best would be to add the values from data
            ladderstep.append(meanm)
        if xlevel[k]==1 and zlevel[k]==0:
            if cstate==state[0]:
                patternA[0].append(ladderstep)
                cstate=state[0]
            elif cstate==state[1]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[2]:
                patternA[1].append(ladderstep)
                cstate=state[3]
            elif cstate==state[3]:
                patternA[1].append(ladderstep)
                cstate=state[3]
            elif cstate==state[4]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[5]:
                patternA[0].append(ladderstep)
                cstate=state[0]
            else:
                raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
        elif xlevel[k]==0 and zlevel[k]==1:
            if cstate==state[0]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[1]:
                patternB[1].append(ladderstep)
                cstate=state[2]
            elif cstate==state[2]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[3]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[4]:
                patternB[0].append(ladderstep)
                cstate=state[5]
            elif cstate==state[5]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            else:
                raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
        elif xlevel[k]==1 and zlevel[k]==1:
            if cstate==state[0]:
                patternC[0].append(ladderstep)
                cstate=state[1]
            elif cstate==state[1]:
                patternC[1].append(ladderstep)
                cstate=state[4]
            elif cstate==state[2]:
                patternC[1].append(ladderstep)
                cstate=state[4]
            elif cstate==state[3]:
                patternC[1].append(ladderstep)
                cstate=state[4]
            elif cstate==state[4]:
                patternC[0].append(ladderstep)
                cstate=state[1]
            elif cstate==state[5]:
                patternC[0].append(ladderstep)
                cstate=state[1]
            else:
                raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
        else:
            raise ValueError('The values of level should be 0s or 1s. (check if zlevel and xlevel are not both 0 for same i)')

    #we crop the sets so every sample are same length
    lref=len(patternA[0][0])
    for ind in [patternA[0],patternA[1],patternB[0],patternB[1],patternC[0],patternC[1]]:
        for i in range(len(ind)):
            if len(ind[i])<lref:
                lref=len(ind[i])
                for j in range(i):
                    ind[j].pop()
            while len(ind[i])>lref:
                ind[i].pop()

    return patternA,patternB,patternC