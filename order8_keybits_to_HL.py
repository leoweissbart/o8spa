#converts the key bits order into high/low levels of power trace
def order8_keybits_to_HL(keybits):
    state=[0,1,2,3,4,5]#0:(0,P), 1:(P,2P), 2:(P,4P), 3:(P,0), 4:(2P,P), 5:(4P,P)
    cstate=0#indicate the current state
    X,Z=[],[]#lists of the outputs with x and z levels
    pattern=[]

    for i in range(len(keybits)):
        if cstate==0:
            if keybits[i]==0:
                X.append(1)
                Z.append(0)
                pattern.append('A')
                cstate=state[0]
            elif keybits[i]==1:
                X.append(1)
                Z.append(1)
                pattern.append('C')
                cstate=state[1]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        elif cstate==1:
            if keybits[i]==0:
                X.append(1)
                Z.append(1)
                pattern.append('C')
                cstate=state[4]
            elif keybits[i]==1:
                X.append(0)
                Z.append(1)
                pattern.append('B')
                cstate=state[2]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        elif cstate==2:
            if keybits[i]==0:
                X.append(1)
                Z.append(1)
                pattern.append('C')
                cstate=state[4]
            elif keybits[i]==1:
                X.append(1)
                Z.append(0)
                pattern.append('A')
                cstate=state[3]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        elif cstate==3:
            if keybits[i]==0:
                X.append(1)
                Z.append(1)
                pattern.append('C')
                cstate=state[4]
            elif keybits[i]==1:
                X.append(1)
                Z.append(0)
                pattern.append('A')
                cstate=state[3]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        elif cstate==4:
            if keybits[i]==0:
                X.append(0)
                Z.append(1)
                pattern.append('B')
                cstate=state[5]
            elif keybits[i]==1:
                X.append(1)
                Z.append(1)
                pattern.append('C')
                cstate=state[1]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        elif cstate==5:
            if keybits[i]==0:
                X.append(1)
                Z.append(0)
                pattern.append('A')
                cstate=state[0]
            elif keybits[i]==1:
                X.append(1)
                Z.append(1)
                pattern.append('C')
                cstate=state[1]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        else:
            raise ValueError('The state of the algorithm is indeterminate please check function : order8_keybits_to_HL')
    return X,Z,pattern