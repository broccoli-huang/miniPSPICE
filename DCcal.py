import numpy as np
import copy

def DCcalculator(NODE_pre,SOURCE_pre,R_LST_pre,L_LST_pre,C_LST_pre):
    R = []
    V = []

    NODE = sorted(NODE_pre)
    N = copy.deepcopy(NODE)
    
    SOURCE = [i if i[1]<i[2] else (-i[0],i[2],i[1]) for i in SOURCE_pre]
    R_LST = [i if i[1]<i[2] else (i[0],i[2],i[1]) for i in R_LST_pre]
    L_LST = [i if i[1]<i[2] else (i[0],i[2],i[1]) for i in L_LST_pre]
    C_LST = [i if i[1]<i[2] else (i[0],i[2],i[1]) for i in C_LST_pre]

    for l in L_LST: #Constrain that l[1] < l[2].
        for r in R_LST:
            if not (r[1] == l[1] and r[2] == l[2]): # in case l and r in parallel
                if r[1] == l[2] and (r[0], l[1], r[2]) not in R:
                    R.append((r[0], l[1], r[2]))
                elif r[2] == l[2] and (r[0], r[1], l[1]) not in R:
                    R.append((r[0], r[1], l[1]))
                elif r not in R:
                    R.append(r)
        for v in SOURCE:
            if not (v[1] == l[1] and v[2] == l[2]):
                if v[1] == l[2]:
                    V.append((v[0], l[1], v[2]))
                elif v[2] == l[2]:
                    V.append((v[0], v[1], l[1]))
                else:
                    V.append(v)
        for n in N:
            if n == l[2]: N.remove(n)
    for l in L_LST:
        for r in R:
            if (r[1] == l[1] and r[2] == l[2]) or (r[1] == l[2] and r[2] == l[1]):
                R.remove(r)

    n_left = copy.deepcopy(N)
    n_removed = []
    
    for i in V:
        for j in i:
            for k in n_left:
                if j == k:
                    n_removed.append(k)
                    n_left.remove(k)
    
    NODE_V = np.zeros(len(NODE))
    node_v = np.zeros(len(N))
    NODE_I = np.zeros(len(N))
    G = np.zeros((len(N), len(N)))

    for i in n_left:
        for j in N:
            if i == j:
                for r in R:
                    if r[1] == i or r[2] == i:
                        G[N.index(i)][N.index(j)] += 1/r[0]
            elif i != j:
                for r in R:
                    if r[1] == i and r[2] == j:
                        G[N.index(i)][N.index(j)] = -1/r[0]
                    elif r[1] == j and r[2] == i:
                        G[N.index(i)][N.index(j)] = -1/r[0]
 
    for i in n_removed:
        for j in n_removed:   #if n_removed.index(i) < n_removed.index(j):
            if n_removed.index(i) < n_removed.index(j):
                for v in V:
                    if v[1] == i and v[2] == j:  #Find the target voltage.
                        G[N.index(i)][N.index(i)] = 1
                        G[N.index(i)][N.index(j)] = -1
                        NODE_I[N.index(i)] = v[0]
                        for r in R:
                            if r[1] == i or r[1] == j or r[2] == i or r[2] == j:
                                G[N.index(j)][N.index(r[1])] += 1/r[0]
                                G[N.index(j)][N.index(r[2])] = -1/r[0]

    #print(G)
    if np.linalg.det(G) != 0:
        node_v = np.linalg.inv(G).dot(NODE_I.T).T
    else:
        node_v[0] = SOURCE[0][0]
        node_v[1] = 0

    for l in L_LST:
        for node in N:
            NODE_V[NODE.index(node)] = copy.deepcopy(node_v[N.index(node)])
        for node in NODE:
            if l[2] == node:
                NODE_V[NODE.index(l[2])] = copy.deepcopy(NODE_V[NODE.index(l[1])])

    node_ground = SOURCE[0][2]
    v_ground = NODE_V[NODE.index(node_ground)]
    NODE_V -= v_ground
    #print(NODE_V)

    NODE_V_ret = []
    for i in NODE_pre:
        NODE_V_ret.append(NODE_V[NODE.index(i)])
    return NODE_V_ret
        
