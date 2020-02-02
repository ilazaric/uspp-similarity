import numpy as np
from Similarity import Similarity

def check(G, k):
    n = len(G)
    K = np.ones((2, 2)) - np.eye(2)
    S = Similarity(G, K)
    v = S[0]

    Gb = (G == 1)

    candidates = np.array([True] * n)
    
    for _ in range(k):
        if not np.any(candidates):
            return False
        
        subindex = np.argmax(v[candidates])
        index = np.arange(n)[candidates][subindex]

        candidates = np.logical_and(candidates, Gb[index])
        candidates[index] = False # just in case

    return True

def MaxClique(G):
    n = len(G)
    for i in range(2,n+1):
        if check(G, i) is False:
            return i-1
    return n

def GenerateMatrix(n, E):
    G = np.zeros((n, n))
    for i,j in E:
        G[i,j] = 1
        G[j,i] = 1
    return G

def GenerateMatrixDirected(n, E):
    G = np.zeros((n, n))
    for i,j in E:
        G[i,j] = 1
    return G
