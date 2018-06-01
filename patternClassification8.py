import numpy as np
import matplotlib.pyplot as plt
def patternClassification8(data,ladderstep,xlevel,zlevel):
    A,B,C=[],[],[]
    m=[]#temporary trace constructed to be stored in A, B or C
    k=0
    run=0
    for i in range(len(data)):
        if ladderstep[i]>3:
            run=1
            m.append(data[i])
        if run==1:
            if ladderstep[i]<3:
                run=0
                # t=np.linspace(0,len(m)-1,len(m))
                # plt.figure()
                # plt.plot(t,m)
                # plt.show()
                if xlevel[k]==1 and zlevel[k]==0:
                    A.append(m)
                    m=[]
                elif xlevel[k]==0 and zlevel[k]==1:
                    B.append(m)
                    m=[]
                elif xlevel[k]==1 and zlevel[k]==1:
                    C.append(m)
                    m=[]
                else:
                    raise ValueError('The values of level should be 0s or 1s. (check if zlevel and xlevel are not both 0 for same i)')
                k+=1
    #we crop the sets so every sample are same length
    lref=len(A[0])
    for i in range(len(A)):
        if len(A[i])<lref:
            lref=len(A[i])
            for j in range(i):
                A[j].pop()
        while len(A[i])>lref:
            A[i].pop()
    lref=len(B[0])
    for i in range(len(B)):
        if len(B[i])<lref:
            lref=len(B[i])
            for j in range(i):
                B[j].pop()
        while len(B[i])>lref:
            B[i].pop()
    lref=len(C[0])
    for i in range(len(C)):
        if len(C[i])<lref:
            lref=len(C[i])
            for j in range(i):
                C[j].pop()
        while len(C[i])>lref:
            C[i].pop()
    return A,B,C