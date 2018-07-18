def order8_HL_to_keybits(xlevel,zlevel):
    state=[0,1,2,3,4,5]#0:(0,P), 1:(P,2P), 2:(P,4P), 3:(P,0), 4:(2P,P), 5:(4P,P)
    cstate=0#indicate the current state
    keybits=[]

    for x,z in zip(xlevel,zlevel):
        if x==1 and z==0:
            if cstate==state[0]:
                keybits.append(0)
                cstate=state[0]
            elif cstate==state[1]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[2]:
                keybits.append(1)
                cstate=state[3]
            elif cstate==state[3]:
                keybits.append(1)
                cstate=state[3]
            elif cstate==state[4]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[5]:
                keybits.append(0)
                cstate=state[0]
            else:
                raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
        elif x==0 and z==1:
            if cstate==state[0]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[1]:
                keybits.append(1)
                cstate=state[2]
            elif cstate==state[2]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[3]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            elif cstate==state[4]:
                keybits.append(0)
                cstate=state[5]
            elif cstate==state[5]:
                raise ValueError('State unreachable, please refere to order 8 algorithm')
            else:
                raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
        elif x==1 and z==1:
            if cstate==state[0]:
                keybits.append(1)
                cstate=state[1]
            elif cstate==state[1]:
                keybits.append(0)
                cstate=state[4]
            elif cstate==state[2]:
                keybits.append(0)
                cstate=state[4]
            elif cstate==state[3]:
                keybits.append(0)
                cstate=state[4]
            elif cstate==state[4]:
                keybits.append(1)
                cstate=state[1]
            elif cstate==state[5]:
                keybits.append(1)
                cstate=state[1]
            else:
                raise ValueError('The state of the algorithm is indeterminate please check function : order8_HL_to_keybits')
        else:
            raise ValueError('The values of level should be 0s or 1s. (check if zlevel and xlevel are not both 0 for same i)')
    return keybits