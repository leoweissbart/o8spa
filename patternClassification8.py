import numpy as np
import matplotlib.pyplot as plt

#morepatterns best fit is for 6 patterns (A1,A2,B1,B2,C1,C2)
def patternClassification8_v3(data,ladderstep,x,z):
    patternA=[[],[]]
    patternB=[[],[]]
    patternC=[[],[]]
    cstate=1
    state=[1,2,3,4,5,6]
    m=[]#temporary trace constructed to be stored in patternA, B or C
    k=0
    run=0
    for i in range(len(data)):
        if ladderstep[i]>3:
            run=1
            m.append(data[i])
        if run==1:
            if ladderstep[i]<3:
                run=0
                if x[k]==1 and z[k]==0:
                    if cstate==state[0]:
                        patternA[0].append(m)
                        cstate=state[0]
                    elif cstate==state[1]:
                        raise ValueError('State unreachable, please refere to order 8 algorithm')
                    elif cstate==state[2]:
                        patternA[1].append(m)
                        cstate=state[3]
                    elif cstate==state[3]:
                        patternA[1].append(m)
                        cstate=state[3]
                    elif cstate==state[4]:
                        raise ValueError('State unreachable, please refere to order 8 algorithm')
                    elif cstate==state[5]:
                        patternA[0].append(m)
                        cstate=state[0]
                    else:
                        raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
                elif x[k]==0 and z[k]==1:
                    if cstate==state[0]:
                        raise ValueError('State unreachable, please refere to order 8 algorithm')
                    elif cstate==state[1]:
                        patternB[1].append(m)
                        cstate=state[2]
                    elif cstate==state[2]:
                        raise ValueError('State unreachable, please refere to order 8 algorithm')
                    elif cstate==state[3]:
                        raise ValueError('State unreachable, please refere to order 8 algorithm')
                    elif cstate==state[4]:
                        patternB[0].append(m)
                        cstate=state[5]
                    elif cstate==state[5]:
                        raise ValueError('State unreachable, please refere to order 8 algorithm')
                    else:
                        raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
                elif x[k]==1 and z[k]==1:
                    if cstate==state[0]:
                        patternC[0].append(m)
                        cstate=state[1]
                    elif cstate==state[1]:
                        patternC[1].append(m)
                        cstate=state[4]
                    elif cstate==state[2]:
                        patternC[1].append(m)
                        cstate=state[4]
                    elif cstate==state[3]:
                        patternC[1].append(m)
                        cstate=state[4]
                    elif cstate==state[4]:
                        patternC[0].append(m)
                        cstate=state[1]
                    elif cstate==state[5]:
                        patternC[0].append(m)
                        cstate=state[1]
                    else:
                        raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
                else:
                    raise ValueError('The values of level should be 0s or 1s. (check if zlevel and xlevel are not both 0 for same i)')
                m=[]
                k+=1
    #we crop the sets so every sample are same length
    lref=len(patternA[0][0])
    for i in range(len(patternA[0])):
        if len(patternA[0][i])<lref:
            lref=len(patternA[0][i])
            for j in range(i):
                patternA[0][j].pop()
        while len(patternA[0][i])>lref:
            patternA[0][i].pop()
    # lref=len(patternA[0])
    for i in range(len(patternA[1])):
        if len(patternA[1][i])<lref:
            lref=len(patternA[1][i])
            for j in range(i):
                patternA[1][j].pop()
        while len(patternA[1][i])>lref:
            patternA[1][i].pop()
    # lref=len(patternB[0][0])
    for i in range(len(patternB[0])):
        if len(patternB[0][i])<lref:
            lref=len(patternB[0][i])
            for j in range(i):
                patternB[0][j].pop()
        while len(patternB[0][i])>lref:
            patternB[0][i].pop()
    # lref=len(patternB[1][0])
    for i in range(len(patternB[1])):
        if len(patternB[1][i])<lref:
            lref=len(patternB[1][i])
            for j in range(i):
                patternB[1][j].pop()
        while len(patternB[1][i])>lref:
            patternB[1][i].pop()
    # lref=len(patternC[0][0])
    for i in range(len(patternC[0])):
        if len(patternC[0][i])<lref:
            lref=len(patternC[0][i])
            for j in range(i):
                patternC[0][j].pop()
        while len(patternC[0][i])>lref:
            patternC[0][i].pop()
    # lref=len(patternC[1][0])
    for i in range(len(patternC[1])):
        if len(patternC[1][i])<lref:
            lref=len(patternC[1][i])
            for j in range(i):
                patternC[1][j].pop()
        while len(patternC[1][i])>lref:
            patternC[1][i].pop()
    return patternA,patternB,patternC
