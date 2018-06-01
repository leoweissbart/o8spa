import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#takes the filtered data and the trigger signal for entire SCM and the 2 model of pattern to return levels detected on the trace
def correlation_vs_model8_v1(data,trigger,modelA,modelB,modelC):
    i,it=0,0
    allseg,seg=[],[]
    while trigger[it]<3.5:#we use the trigger to find the beginning of ML algorithm
        it+=1 
    i=int(it)
    for k in range(256):
        for j in range(len(modelA)):
            i=int(it)
            seg.append(data[i])
            it+=1
        it+=1.4335#during ML algorithm 70254 points are captured and there is 256 laddersteps : 70254/256=274.43 and substract the length of the model
        seg-=np.mean(seg)
        allseg.append(seg)
        seg=[]

    array_corrA,array_corrB,array_corrC=[],[],[]
    t=np.linspace(0,len(modelA)-1,len(modelA))
    for i in range(len(allseg)):
        # if i>60:
        # plt.figure()
        # plt.plot(t,allseg[i],t,modelA,'r',t,modelB,'b',t,modelC,'g')#,t,modelA,'b',t,modelB,'tab:orange',t,modelC,'g'
        # plt.legend(('seg','modelA','modelB','modelC'),loc='best')
        # plt.show()
        corrC=np.correlate(allseg[i],modelC)
        corrB=np.correlate(allseg[i],modelB)
        corrA=np.correlate(allseg[i],modelA)
        # print('corrA=',corrA)
        # print('corrC=',corrC)
        # plt.show()
        array_corrC.append(corrC)
        array_corrB.append(corrB)
        array_corrA.append(corrA)
    array_corrA-=np.mean(array_corrA)
    array_corrB-=np.mean(array_corrB)
    array_corrC-=np.mean(array_corrC)
    array_corrC+=0.002#gitan forrain no jutsu

    t=np.linspace(0,len(array_corrA)-1,len(array_corrA))
    fig=plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 256, 1))
    plt.title('Correlation')
    plt.scatter(t,array_corrA)
    plt.scatter(t,array_corrB)
    plt.scatter(t,array_corrC)
    plt.plot(t,array_corrA,'#1f77b4',t,array_corrB,'#ff7f0e',t,array_corrC,'#2ca02c')
    plt.xlabel('Number of ladderstep')
    plt.ylabel('Correlation level')
    plt.legend(('Correlation with model A','Correlation with model B','Correlation with modelC'),loc='best')

    ax = subplot(111)

    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.grid(True,'minor')
    ax.xaxis.grid(True,'major',linewidth=2)

    xlevel,zlevel=[],[]
    pattern=[]
    for i in range(len(array_corrA)):
        if array_corrA[i]>array_corrB[i] and array_corrA[i]>array_corrC[i]:
            xlevel.append(1)
            zlevel.append(0)
            pattern.append('A')
        elif array_corrB[i]>array_corrA[i] and array_corrB[i]>array_corrC[i]:
            xlevel.append(0)
            zlevel.append(1)
            pattern.append('B')
        elif array_corrC[i]>array_corrA[i] and array_corrC[i]>array_corrB[i]:
            xlevel.append(1)
            zlevel.append(1)
            pattern.append('C')
        else:
            xlevel.append(2)#if there is problem with comparaison
            zlevel.append(2)
            pattern.append('E')
    
    return xlevel,zlevel,pattern