import numpy as np
import matplotlib.pyplot as plt
from pylab import subplot
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
  
#model is an array of every patterns models should be 6 patterns for order 8 attack for 6 patterns
def correlation_vs_model8_6patterns(data,trigger,model):
    i,it=0,0
    allseg,seg=[],[]
    while trigger[it]>-2:#we use the trigger to find the beginning of ML algorithm
        it+=1
    it+=3263#to don't consider the  part before the laddersteps
    j=it
    n_points=0
    while trigger[j]<-2:
        n_points+=1
        j+=1
    i=int(it)
    #we separate all the laddersteps in the dataset into 'allseg'
    for k in range(256):
        for j in range(len(model[0])):
            i=int(it)
            seg.append(data[i])
            it+=1
        it+=1.13#weighting to always fit with the laddersteps
        seg=(seg-np.mean(seg))/(np.std(seg))#normalization by Z-score of the segments
        allseg.append(seg)
        seg=[]
    
     #compute correlation for every models
    array_corr=[]
    for i in range(len(model)):
        array_corr.append([])
    
    for i in range(len(allseg)):
        for elmt in range(len(array_corr)):
            array_corr[elmt].append(np.correlate(allseg[i],model[elmt]))
#######################################################################################################################################
    t=np.linspace(0,len(array_corr[0])-1,len(array_corr[0]))
    plt.figure()
    plt.title('Correlation')
    for ind in range(len(array_corr)):
        plt.plot(t,array_corr[ind])
    plt.xlabel('Time (in Second)')
    plt.ylabel('Correlation level')
    plt.grid()
    plt.legend(('A1','A2','B1','B2','C1','C2'),loc='best')


    t=np.linspace(0,len(array_corr[0])-1,len(array_corr[0]))
    fig=plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 256, 1))
    plt.title('Correlation')
    for ind in range(len(array_corr)):
        plt.scatter(t,array_corr[ind])
    for ind in range(len(array_corr)):
        plt.plot(t,array_corr[ind])
    plt.xlabel('Number of ladderstep')
    plt.ylabel('Correlation level')
    plt.legend(('A1','A2','B1','B2','C1','C2'),loc='best')

    ax = subplot(111)

    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.grid(True,'minor')
    ax.xaxis.grid(True,'major',linewidth=2)
#################################################################################################################################
    xlevel,zlevel=[],[]
    pattern=[]
    for i in range(len(array_corr[0])):
        if array_corr[0][i]==max([array_corr[0][i],array_corr[1][i],array_corr[2][i],array_corr[3][i],array_corr[4][i],array_corr[5][i]]) or  array_corr[1][i]==max([array_corr[0][i],array_corr[1][i],array_corr[2][i],array_corr[3][i],array_corr[4][i],array_corr[5][i]]):
            xlevel.append(1)
            zlevel.append(0)
            pattern.append('A')
        elif array_corr[2][i]==max([array_corr[0][i],array_corr[1][i],array_corr[2][i],array_corr[3][i],array_corr[4][i],array_corr[5][i]]) or array_corr[3][i]==max([array_corr[0][i],array_corr[1][i],array_corr[2][i],array_corr[3][i],array_corr[4][i],array_corr[5][i]]):
            xlevel.append(0)
            zlevel.append(1)
            pattern.append('B')
        elif array_corr[4][i]==max([array_corr[0][i],array_corr[1][i],array_corr[2][i],array_corr[3][i],array_corr[4][i],array_corr[5][i]]) or array_corr[5][i]==max([array_corr[0][i],array_corr[1][i],array_corr[2][i],array_corr[3][i],array_corr[4][i],array_corr[5][i]]):
            xlevel.append(1)
            zlevel.append(1)
            pattern.append('C')
        else:
            raise ValueError('This state is not an actual state in the algorithm, please check correlation_vs_model8.py')
    
    return xlevel,zlevel,pattern
