from Similarity import *
from CliqueSolver import MaxClique, GenerateMatrix, GenerateMatrixDirected
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

def check1():
    A = np.zeros((5, 5))
    B = np.zeros((3, 3))
    for i,j in [(0,1), (1,2)]:
        B[i,j] = 1
    for i,j in [(0,1), (0,2), (1,2), (1,4), (2,3), (2,4), (3,1)]:
        A[i,j] = 1
    S = Similarity(B, A)
    print(S)


def check2():
    A = np.zeros((4, 4))
    B = np.zeros((6, 6))
    for i,j in [(0,1), (1,0), (1,2), (2,1), (0,2), (3,0), (3,2)]:
        A[i,j] = 1
    for i,j in [(0,3), (5,3), (1,3), (1,5), (5,0), (5,2), (2,5), (0,2), (2,0), (2,4)]:
        B[i,j] = 1
    S = Similarity(A, B)
    print(S)

def check3(m, n):
    A = np.zeros((m+n+1, m+n+1))
    for i in range(m):
        A[i+1,0] = 1
    for j in range(n):
        A[0,m+1+j] = 1
    S = HubCenterAuthority(A)
    print(S)

# check1()
# check2()
# check3(3,5)

# G = GenerateMatrix(5, [(0, 1), (1, 2), (2, 3), (1, 4), (1, 3)])
# print(G)
# print(MaxClique(G))

def cliques():
    with open('frb30-15-clq/frb30-15-1.clq', 'r') as f:
        lines = f.read().split('\n')
    
    V = int(lines[0].split(' ')[2])
    E = []
    for line in lines[1:]:
        splitted = line.split(' ')
        if len(splitted) == 1: break
        i, j = int(splitted[1])-1, int(splitted[2])-1
        E.append((i, j))

    # print(V, len(E))

    G = GenerateMatrix(V, E)
    print(MaxClique(G))

# cliques()

def neighborhood(E, start, distance, safety = 1e9):
    D = {}
    Di = {}
    for i,j in E:
        if i not in D:
            D[i] = []
        if j not in Di:
            Di[j] = []
        D[i].append(j)
        Di[j].append(i)

    def deg(a):
        bla = 0
        if a in D: bla += len(D[a])
        if a in Di: bla += len(Di[a])
        return bla

    subset = {start}
    for _ in range(distance-1):
        sets = []
        for a in subset:
            if deg(a) > safety: continue
            if a in D: sets.append(D[a])
            if a in Di: sets.append(Di[a])
        subset = subset.union(*sets)

    return subset

def clamp(x): 
  return max(0, min(int(x), 255))

def to_rgb(r, g, b):
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))


def stanford(start, dist, safety = 1e9):
    with open('web-Stanford.txt', 'r') as f:
        lines = f.read().split('\n')
    
    E = []
    for line in lines[1:]:
        splitted = line.split()
        if len(splitted) <= 1: continue
        if splitted[0] == '#':
            if splitted[1] == 'Nodes:':
                V = int(splitted[2])
            continue
        i, j = int(splitted[0])-1, int(splitted[1])-1
        E.append((i, j))

    print(V, len(E))
    subset = neighborhood(E, start, dist, safety = safety)
    subE = [(i, j) for i, j in E if i in subset and j in subset]
    print(len(subset), len(subE))

    # graph = nx.DiGraph()
    # graph.add_nodes_from(subset)
    # graph.add_edges_from(subE)
    # nx.draw(graph, node_size = 15)
    # plt.show()

    rel = {}
    for idx, node in enumerate(subset):
        rel[node] = idx
    relE = [(rel[i], rel[j]) for i, j in subE]

    G = GenerateMatrixDirected(len(rel), relE)
    S = HubCenterAuthority(G, num_steps = 5000)
    hub = S[0] / S.max()
    center = S[1] / S.max()
    authority = S[2] / S.max()
    colors = [to_rgb(255*(1-c), 255*c, 0) for h, c, a in zip(hub, center, authority)]

    # print('hub: ', hub[hub.argsort()[-10:][::-1]])
    # print('center: ', center[center.argsort()[-10:][::-1]])
    # print('authority: ', authority[authority.argsort()[-10:][::-1]])

    # print(len(colors))
    # print(colors)

    graph = nx.DiGraph()
    graph.add_nodes_from(range(len(rel)))
    graph.add_edges_from(relE)
    nx.draw(graph, pos=nx.spring_layout(graph), node_size = 25, node_color = colors)
    plt.show()

    
# stanford(70493, 7, safety = 30)
# stanford(1010, 3)
# stanford(92101, 3, safety = 50)
# stanford(39210, 10, safety = 50)
stanford(57439, 7, safety = 50)
