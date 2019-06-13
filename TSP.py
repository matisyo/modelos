
# coding: utf-8

# In[1]:


data = """0,1,1
0,6,1
1,2,1
2,3,1
3,4,1
4,5,1
4,8,1
4,13,1
5,9,1
5,20,1
6,10,1
7,8,1
7,11,1
9,13,1
10,11,1
10,14,1
12,14,1
12,19,1
13,18,1
13,17,1
14,15,1
15,16,1
16,17,1
18,22,1
19,24,1
20,22,1
21,22,1
22,23,1
23,24,1"""


# # Armo grafo todos contra todos

# In[2]:


N=25


# In[3]:


caminos_lista = []
for linea in data.split("\n"):
    a,b,w =[int(i) for i in linea.split(',')]  
    caminos_lista.append([a,b,w])


# In[4]:


from math import inf
from itertools import product
 
def floyd_warshall(n, edge):
    rn = range(n)
    dist = [[inf] * n for i in rn]
    nxt  = [[0]   * n for i in rn]
    for i in rn:
        dist[i][i] = 0
    for u, v, w in edge:
        dist[u][v] = w
        dist[v][u] = w
        nxt[u][v] = v
        nxt[v][u] = u
        
    for k, i, j in product(rn, repeat=3):
        sum_ik_kj = dist[i][k] + dist[k][j]
        if dist[i][j] > sum_ik_kj:
            dist[i][j] = sum_ik_kj
            nxt[i][j]  = nxt[i][k]
    return nxt,dist
caminos,dist = floyd_warshall(N, caminos_lista)


# In[5]:


for i,fila in enumerate(dist):
    print(chr(i+ord('A'))+" "+" ".join(map(str,fila)).replace("0","."))


# In[34]:


import numpy as np
memo = (np.ones(N*2**N)*500).reshape(N,2**N)


# In[6]:


combinations = {}
for i in range(2**N):
    k = bin(i).count("1")
    t = combinations.get(k,set())
    t.add(i)
    combinations[k] = t


# # TSP

# In[75]:


infinito = 50000
def setup(S):
    # calculo la altura 2
    for i in range(N):
        if i!=S:
            memo[i][1<<S|1<<i] = 0#dist[S][i] en 0 no es ciclo y empezas en el 2do

def notIn(i,subset):
    return ((1 << i )& subset)==0
def solve(S):
    # ya tengo precalculado altura 1 y 2
    # la altura 1 es el nodo final con peso 0
    # la altura 2 es desde todos los nodos hacia el nodo final
    # sigo desde la altura 3 
    for r in range(3,N+1):
        for subset in combinations[r]:# comb[3] --> {0000111,0001011,0101010,...}
            #solo quiero volver a S en el final por eso evito esos
            if notIn(S, subset):
                continue
            for prox in range(N):
                #itero por los del subset
                if prox == S or notIn(prox,subset):
                    continue
                # lo saco del subet entonces me queda un subset de altura menor
                # es decir si estoy en r = 3 mi state es de 2 cosas entonces lo tngo precalculado
                # en memo
                state = subset ^ (1 << prox)
                minDist = infinito
                for e in range(N):
                    #calculo el minimo de ir a prox con la suma del estado que ya tenia calculado 
                    #de la altura anterior
                    if e == S or e == prox or notIn(e, subset):
                         continue
                    newDist = memo[e][state] + dist[e][prox]
                    if newDist < minDist:
                        minDist=newDist
                #actualizo con el menor peso
                memo[prox][subset] = minDist

def findMinCost(S):
    end_state = (1<<N) -1
    minTourCost = infinito
    for e in range(N):
        if e ==S:
            continue
        tourCost = memo[e][end_state] + dist[e][S] #cerrar ciclo
        if tourCost < minTourCost:
            minTourCost = tourCost
    return minTourCost

def findOptimalTour(S):
    lastIndex = S
    state = (1 << N) -1
    tour = [i for i in range(N+1)]
    
    for k in range(1,N):
        i = N-k
        index = -1
        for j in range(N):
            if j == S or notIn(j,state):
                continue
            if index == -1:
                index = j
            prevDist = memo[index][state] + dist[index][lastIndex]
            newDist = memo[j][state] + dist[j][lastIndex]
            if newDist<prevDist:
                index = j
        tour[i] = index
        state = state ^ (1 << index)
        lastIndex = index
        
    tour[0] = tour[N] = S
    return tour
        
def sumar_camino(lista):
    sumar = 0
    for x,y in zip(lista[:-1],lista[1:]):
        sumar += dist[x][y]
        #print(x,y,dist[x][y])
    return sumar                


# In[76]:


setup(0)
solve(0)
findMinCost(0)
tur = findOptimalTour(0)


# In[79]:


camino_optimo_glpk="""
B 0
C 1
D 2
E 18
F 3
G 22
H 20
I 19
J 4
K 23
L 21
M 11
N 5
O 10
P 9
Q 8
R 7
S 6
T 12
U 17
V 16
W 15
X 14
Y 13
"""

camino_optimo_glpk="""
B 0
C 1
D 2
E 18
F 3
G 22
H 20
I 19
J 4
K 23
L 21
M 11
N 5
O 10
P 9
Q 8
R 7
S 6
T 12
U 17
V 16
W 15
X 14
Y 13
"""
b = list(map(lambda x: ord(x.split()[0])-ord('A'),sorted(camino_optimo_glpk.split("\n")[1:-1],key=lambda x: int(x.split()[1])) ))


# In[80]:


print(f"Camino optimo con dp: {sumar_camino(tur)}\nCamino optimo glpk: {sumar_camino([0]+b+[0])}")
print(" ".join(map(str,tur)))
print(" ".join(map(str,[0]+b+[0])))

