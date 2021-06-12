from vpython import*
import numpy as np
import math
   
def ACcalculator(NODE,SOURCE,R_LST,L_LST,C_LST,freq):
    PI = math.pi

    node_num = len(NODE)
    R_num = len(R_LST)
    L_num = len(L_LST)
    C_num = len(C_LST)


    def imp(n1, n2):#return兩node間電導
        Y = 0 + 0j
        for R in R_LST:
            if (R[1] == n1 and R[2] == n2) or (R[1] == n2 and R[2] == n1):
                Y = Y+1/R[0]
        for L in L_LST:
            if (L[1] == n1 and L[2] == n2) or (L[1] == n2 and L[2] == n1):
                Y = Y-1/(2*PI*freq*L[0])*1j
        for C in C_LST:
            if (C[1] == n1 and C[2] == n2) or (C[1] == n2 and C[2] == n1):
                Y = Y+2*PI*freq*C[0]*1j
        return Y

    def series(n):#return和n相鄰的所有node之間的電導
        Y = 0 + 0j
        for R in R_LST:
            if R[1] == n or R[2] == n:
                Y = Y + imp(R[1], R[2])
        for L in L_LST:
            if L[1] == n or L[2] == n:
                Y = Y + imp(L[1], L[2])
        for C in C_LST:
            if C[1] == n or C[2] == n:
                Y = Y + imp(C[1], C[2])
        return Y


    L1 = []
    L2 = []#此處L1矩陣*電壓矩陣=L2矩陣
    N_Vplus = SOURCE[2]
    N_Vminus = SOURCE[3]
    Vplus = SOURCE[0] * math.cos(SOURCE[1]/180*PI) + SOURCE[0] * math.sin(SOURCE[1]/180*PI)*1j
    Vminus = 0
    for i in range(node_num):
        L = []
        if NODE[i] == N_Vplus or NODE[i] == N_Vminus:
            continue
        for j in range(node_num):
            if NODE[j] == N_Vplus or NODE[j] == N_Vminus:
                continue
            if j == i:
                L.append(series(NODE[i]))
                continue
            L.append((-1) * imp(NODE[i], NODE[j]))
        L1.append(L)
    for i in range(node_num):
        L = []
        if NODE[i] == N_Vplus or NODE[i] == N_Vminus:
            continue
        I = Vplus * imp(N_Vplus, NODE[i]) + Vminus* imp(N_Vminus, NODE[i])
        L.append(I)
        L2.append(L)
    M1 = np.array(L1)#轉型態為矩陣
    M2 = np.array(L2)
    M1_inverse = np.linalg.inv(M1)
    M_sol = M1_inverse.dot(M2)
    vol_node = []#NODE中的node對應到的電壓

    j = 0
    for i in range(node_num):
        if NODE[i] == N_Vplus:
            vol_node.append(Vplus)
            continue
        if NODE[i] == N_Vminus:
            vol_node.append(Vminus)
            continue
        vol_node.append(M_sol[j][0])
        j = j + 1

        
    vol_node2 = []
    I_R_LST2 = []
    I_L_LST2 = []
    I_C_LST2 = []
    for V in vol_node:
        phasor = []
        VR = V.real
        VI = V.imag
        Amp = abs(V)
        if VR < 0:
            Amp = -Amp
        if VR != 0:
            phas = atan(VI/VR)*180/PI
        elif VI > 0:
            phas = 90
        elif VI < 0:
            phas = -90
        elif VI == 0:
            phas = 0
        phasor.append(Amp)
        phasor.append(phas)
        vol_node2.append(phasor)

    I_R_LST = []#R_LST中的電阻對應到的電流
    I_L_LST = []
    I_C_LST = []
    vol_R = []
    vol_L = []
    vol_C = []

    for R in R_LST:
        n1 = R[1]
        n2 = R[2]
        ind_1 = 0
        ind_2 = 0
        for i in range(node_num):
            if NODE[i] == n1:
                ind_1 = i
            if NODE[i] == n2:
                ind_2 = i
        V = vol_node[ind_1] - vol_node[ind_2]
        t1 = []
        phasor = []
        VR = V.real
        VI = V.imag
        Amp = abs(V)
        if VR < 0:
            Amp = -Amp
        if VR != 0:
            phas = atan(VI/VR)*180/PI
        elif VI > 0:
            phas = 90
        elif VI < 0:
            phas = -90
        elif VI == 0:
            phas = 0
        phasor.append(Amp)
        phasor.append(phas)
        vol_R.append(phasor)
        
        I = V / R[0]
        I_R_LST.append(I)
    for L in L_LST:
        n1 = L[1]
        n2 = L[2]
        ind_1 = 0
        ind_2 = 0
        for i in range(node_num):
            if NODE[i] == n1:
                ind_1 = i
            if NODE[i] == n2:
                ind_2 = i
        V = vol_node[ind_1] - vol_node[ind_2]
        t1 = []
        phasor = []
        VR = V.real
        VI = V.imag
        Amp = abs(V)
        if VR < 0:
            Amp = -Amp
        if VR != 0:
            phas = atan(VI/VR)*180/PI
        elif VI > 0:
            phas = 90
        elif VI < 0:
            phas = -90
        elif VI == 0:
            phas = 0
        phasor.append(Amp)
        phasor.append(phas)
        vol_L.append(phasor)
        
        I = V / (2*PI*freq*L[0]*1j)
        I_L_LST.append(I)
    for C in C_LST:
        n1 = C[1]
        n2 = C[2]
        ind_1 = 0
        ind_2 = 0
        for i in range(node_num):
            if NODE[i] == n1:
                ind_1 = i
            if NODE[i] == n2:
                ind_2 = i
        V = vol_node[ind_1] - vol_node[ind_2]
        t1 = []
        phasor = []
        VR = V.real
        VI = V.imag
        Amp = abs(V)
        if VR < 0:
            Amp = -Amp
        if VR != 0:
            phas = atan(VI/VR)*180/PI
        elif VI > 0:
            phas = 90
        elif VI < 0:
            phas = -90
        elif VI == 0:
            phas = 0
        phasor.append(Amp)
        phasor.append(phas)
        vol_C.append(phasor)
        
        I = V * 2*PI*freq*C[0]*1j
        I_C_LST.append(I)


    '''    
    for I in I_R_LST:
        phasor = []
        IR = I.real
        II = I.imag
        Amp = abs(I)
        if IR < 0:
            Amp = -Amp
        if IR != 0:
            phas = atan(II/IR)*180/PI
        elif II > 0:
            phas = 90
        elif II < 0:
            phas = -90
        elif II == 0:
            phas = 0
        phasor.append(Amp)
        phasor.append(phas)
        I_R_LST2.append(phasor)
    for I in I_L_LST:
        phasor = []
        IR = I.real
        II = I.imag
        Amp = abs(I)
        if IR < 0:
            Amp = -Amp
        if IR != 0:
            phas = atan(II/IR)*180/PI
        elif II > 0:
            phas = 90
        elif II < 0:
            phas = -90
        elif II == 0:
            phas = 0
        phasor.append(Amp)
        phasor.append(phas)
        I_L_LST2.append(phasor)
    for I in I_C_LST:
        phasor = []
        IR = I.real
        II = I.imag
        Amp = abs(I)
        if IR < 0:
            Amp = -Amp
        if IR != 0:
            phas = atan(II/IR)*180/PI
        elif II > 0:
            phas = 90
        elif II < 0:
            phas = -90
        elif II == 0:
            phas = 0
        phasor.append(Amp)
        phasor.append(phas)
        I_C_LST2.append(phasor)
    '''
    '''
    print('NODE:', NODE)
    print('voltage of node', vol_node2)
    print('R_LST: ', R_LST)
    print('voltage of R', vol_R)
    print('L_LST: ', L_LST)
    print('voltage of L', vol_L)
    print('C_LST: ', C_LST)
    print('voltage of C', vol_C)
    '''
    return vol_node2, vol_R, vol_L, vol_C
            
        

    
        
            
            
    
            





